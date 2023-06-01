from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

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
