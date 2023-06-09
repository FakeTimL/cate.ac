from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

'''
class Chapter(models.Model):
  name = models.TextField()

  def __str__(self):
    return self.name
'''


class Topic(models.Model):
  name = models.TextField()
  # chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, default=None)
  resources = models.TextField()

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


class History(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  user_answer = models.TextField()
  gpt_mark = models.IntegerField()
  gpt_comments = models.TextField()

  def __str__(self):
    return str(self.user) + ": " + self.user_answer


class Feedback(models.Model):
  text = models.TextField()
  publish_date = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.text
