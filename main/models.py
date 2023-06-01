from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class Question(models.Model):
  statement = models.TextField()
  mark_scheme = models.TextField()
  gpt_prompt = models.TextField()

  def __str__(self):
    return self.statement


class Feedback(models.Model):
  text = models.TextField()
  publish_date = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.text
