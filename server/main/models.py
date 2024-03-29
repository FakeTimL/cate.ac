from django.db import models
from accounts.models import User


class Feedback(models.Model):
  text = models.TextField()
  email = models.EmailField(blank=True)
  date = models.DateTimeField(auto_now_add=True)

  def __str__(self) -> str:
    return self.email + ': ' + self.text


class Topic(models.Model):
  name = models.TextField()
  parent = models.ForeignKey('self', related_name='children', blank=True, null=True, on_delete=models.SET_NULL)
  resources = models.TextField(blank=True)

  def __str__(self) -> str:
    return self.name


class Question(models.Model):
  statement = models.TextField()
  mark_denominator = models.IntegerField(default=1)
  mark_minimum = models.IntegerField(default=0)
  mark_maximum = models.IntegerField()
  mark_scheme = models.TextField()
  gpt_prompt = models.TextField()
  topics = models.ManyToManyField(Topic, related_name='questions')

  def __str__(self) -> str:
    return self.statement


class Sheet(models.Model):
  user = models.ForeignKey(User, related_name='sheets', on_delete=models.CASCADE)
  questions = models.ManyToManyField(Question, through='SheetQuestion', related_name='sheets')
  time_limit = models.IntegerField()
  name = models.TextField()
  description = models.TextField()

  def __str__(self) -> str:
    return str(self.user) + ': ' + self.name


class SheetQuestion(models.Model):
  sheet = models.ForeignKey(Sheet, on_delete=models.CASCADE)
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  index = models.IntegerField()  # Determines the order of questions in the sheet.


class Submission(models.Model):
  user = models.ForeignKey(User, related_name='submissions', on_delete=models.CASCADE)
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  user_answer = models.TextField()
  gpt_marking = models.BooleanField(default=False)       # True if marking in progress
  gpt_mark = models.IntegerField(blank=True, null=True)  # Blank if yet to be marked
  gpt_comments = models.TextField(blank=True)            # Blank if yet to be marked
  date = models.DateTimeField(auto_now_add=True)

  @property
  def gpt_marked(self) -> bool:
    return self.gpt_mark is not None

  def __str__(self) -> str:
    return str(self.user) + ': ' + self.user_answer


class Attempt(models.Model):
  user = models.ForeignKey(User, related_name='attempts', on_delete=models.CASCADE)
  sheet = models.ForeignKey(Sheet, related_name='attempts', on_delete=models.CASCADE)
  submissions = models.ManyToManyField(Submission, through='AttemptSubmission', related_name='attempt')
  begin_time = models.DateTimeField(auto_now_add=True)
  end_time = models.DateTimeField(blank=True, null=True)

  @property
  def completed(self) -> bool:
    return self.end_time is not None

  def __str__(self) -> str:
    return 'Attempt made by ' + str(self.user) + ' for ' + str(self.sheet)


class AttemptSubmission(models.Model):
  attempt = models.ForeignKey(Attempt, on_delete=models.CASCADE)
  submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
