from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Question(models.Model):
  statement = models.TextField()
  mark_scheme = models.TextField()
  gpt_prompt = models.TextField()

  def __str__(self):
    return self.statement


class Topic(models.Model):
  name = models.TextField()

  def __str__(self):
    return self.name


class History(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  user_answer = models.TextField()
  gpt_mark = models.IntegerField()
  gpt_comments = models.TextField()


class Feedback(models.Model):
  text = models.TextField()
  publish_date = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.text
