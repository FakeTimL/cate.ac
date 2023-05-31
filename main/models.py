from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime, json
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Feedback(models.Model):
  text = models.TextField()
  publish_date = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return self.text


UserModel = get_user_model()

# See specifications of objects and relationships here:
# https://www.notion.so/Problem-Set-User-Study-Information-Database-f0963cb2f5ee4f09ab09cb951f0f63ba


class CommentRoot(models.Model):
  ''' Something that can be commented by users will have a comment root
  '''
  content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
  object_id = models.PositiveIntegerField()
  #content_object = GenericForeignKey('content_type', 'object_id')
  
  class Meta:
    constraints = [
      # Ensures that `CommentRoot.objects.get_or_create` is atomic 
      # https://docs.djangoproject.com/en/3.1/ref/models/querysets/#get-or-create
      models.UniqueConstraint(fields=['content_type', 'object_id'], name='unique_content_object')
    ]


def get_comment_root_for(obj):
  content_type = ContentType.objects.get_for_model(obj)
  root, is_new = CommentRoot.objects.get_or_create(content_type=content_type, object_id=obj.pk)
  return root


class Comment(models.Model):
  ''' User comment
  '''
  root = models.ForeignKey(CommentRoot, on_delete=models.CASCADE, related_name='comments')
  parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True) # Parent comment (the comment being replied; blank for outmost-level comments)
  user = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, related_name='comments')
  text = models.TextField()
  #votes = models.IntegerField(default=0)
  #voters = models.ManyToManyField(UserModel, related_name='voted_comments', blank=True)
  publish_date = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return str(self.user) + ": " + self.text


class Course(models.Model):
  ''' Courses
  '''
  codename = models.SlugField(max_length=100, unique=True) # Use as URLs
  name = models.CharField(max_length=100)
  description = models.TextField(blank=True)
  publish_date = models.DateTimeField(auto_now_add=True)
  last_edited = models.DateTimeField(auto_now=True)
  staff_only = models.BooleanField(default=False)
  
  def course_image_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/main/courses/course_<id>_image
    return 'main/courses/course_{0}_image'.format(instance.id)
  
  image = models.ImageField(upload_to=course_image_path, default='main/placeholder.png')
  
  def __str__(self):
    return self.name
  
  def lecture_last_edited(self):
    res = self.last_edited
    all_lectures = Lecture.objects.filter(course=self.id)
    for lecture in all_lectures:
      if res < lecture.last_edited:
        res = lecture.last_edited
    return res


class Lecture(models.Model):
  ''' Lectures
  '''
  course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='lectures')
  #number = models.IntegerField() # Use on URLs
  title = models.CharField(max_length=100)
  video = models.FileField(upload_to='lecture_videos/', blank=True) # Video tutorial
  lecture_notes = models.TextField(blank=True) # Text material
  lecture_notes_js = models.TextField(blank=True) # Interactive content, JavaScript
  lecture_notes_css = models.TextField(blank=True) # Interactive content, CSS
  author = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, related_name='authored_lectures')
  publish_date = models.DateTimeField(auto_now_add=True)
  last_edited = models.DateTimeField(auto_now=True)
  staff_only = models.BooleanField(default=False)
  
  def __str__(self):
    return str(self.course) + " | " + self.title


class KnowledgeUnit(models.Model):
  ''' Knowledge units
  '''
  text = models.TextField() # e.g. "$\cos60^\circ=\frac{1}{2}$" or "pay attention to essential information in parentheses"
  lectures = models.ManyToManyField(Lecture, related_name='knowledge_units', blank=True)
  
  def __str__(self):
    return self.text


class KnowledgeMap(models.Model):
  ''' Knowledge mind maps
  '''
  data = models.TextField(blank=True) # Data in json format
  
  # Metadata (separate fields are currently unnecessary)
  #ref_knowledge_units = models.ManyToManyField(KnowledgeUnit, related_name='+', blank=True)
  #ref_knowledge_maps = models.ManyToManyField('self', blank=True)
  
  # Permissions
  # TODO: use model inheritance
  owner = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='+')
  users_manage = models.ManyToManyField(UserModel, related_name='+', blank=True)
  users_read = models.ManyToManyField(UserModel, related_name='+', blank=True)
  users_write = models.ManyToManyField(UserModel, related_name='+', blank=True)
  
  def __str__(self):
    return self.name
  
  def manage_permitted(user):
    return user.id == owner.id or users_manage.filter(pk=user.id).exists()
  
  def read_permitted(user):
    return user.id == owner.id or users_read.filter(pk=user.id).exists()
    
  def write_permitted(user):
    return user.id == owner.id or users_write.filter(pk=user.id).exists()


class Question(models.Model):
  ''' Question
  '''
  data = models.TextField() # Data in json format
  
  # Metadata
  TYPE_CHOICES = [ # Use lazy translation here. https://docs.djangoproject.com/en/3.0/topics/i18n/translation/#lazy-translation
    ('choice', _('Multiple Choice')),
    ('fill', _('Fill-in-the-Blanks')),
    ('qa', _('Q&A')),
  ]
  type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='qa')
  lectures = models.ManyToManyField(Lecture, related_name='explained_questions', blank=True)
  knowledge_units = models.ManyToManyField(KnowledgeUnit, related_name='related_questions', blank=True)
  source = models.CharField(max_length=100, blank=True)
  
  def __str__(self):
    return json.loads(self.data).get('statement', self.data)[:50]


class ProblemSet(models.Model):
  ''' Problem sets
  '''
  codename = models.SlugField(max_length=100, unique=True) # Use as URLs
  name = models.CharField(max_length=100) # e.g. "化学（九上）习题集"
  #category = models.CharField(max_length=100) # e.g. "初中化学"
  description = models.TextField(blank=True)
  questions = models.ManyToManyField(Question, related_name='related_problemsets', blank=True)
  
  def __str__(self):
    return self.name


# Learning data for an individual user
# https://www.notion.so/Problem-Set-User-Study-Information-Database-f0963cb2f5ee4f09ab09cb951f0f63ba#ffd5e9884fd749c79849277b71ef6b5c

class QuestionSchedule(models.Model):
  ''' Question scheduler data, through table
  '''
  user_learning_data = models.ForeignKey('UserLearningData', on_delete=models.CASCADE)
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  seed = models.IntegerField() # Random seed
  stage = models.CharField(max_length=50, blank=True)
  time = models.DateTimeField()


class QuestionNotes(models.Model):
  ''' Question notes, through table
  '''
  user_learning_data = models.ForeignKey('UserLearningData', on_delete=models.CASCADE)
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  data = models.TextField(blank=True) # Data in json format
  
  class Meta:
    verbose_name_plural = 'question notes'


class UserLearningData(models.Model):
  user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='learning_data')
  question_schedules = models.ManyToManyField(Question, through=QuestionSchedule, related_name='+', blank=True)
  question_notes = models.ManyToManyField(Question, through=QuestionNotes, related_name='+', blank=True)
  
  class Meta:
    verbose_name_plural = 'user learning data'
  
  def __str__(self):
    return str(self.user) + '\'s learning data'

