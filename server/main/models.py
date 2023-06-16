from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Feedback(models.Model):
  text = models.TextField()
  email = models.EmailField(blank=True)
  publish_date = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.email + ': ' + self.text


class Topic(models.Model):
  name = models.TextField()
  parent = models.ForeignKey('self', related_name='children', blank=True, null=True, on_delete=models.SET_NULL)
  resources = models.TextField(blank=True)

  def __str__(self):
    return self.name


class Question(models.Model):
  statement = models.TextField()
  mark_denominator = models.IntegerField(default=1)
  mark_minimum = models.IntegerField(default=0)
  mark_maximum = models.IntegerField()
  mark_scheme = models.TextField()
  gpt_prompt = models.TextField()
  topics = models.ManyToManyField(Topic, related_name='questions')

  def __str__(self):
    return self.statement


class Submission(models.Model):
  user = models.ForeignKey(User, related_name='submissions', blank=True, null=True, on_delete=models.SET_NULL)
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  user_answer = models.TextField()
  gpt_mark = models.IntegerField()
  gpt_comments = models.TextField()
  date = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return str(self.user) + ": " + self.user_answer
