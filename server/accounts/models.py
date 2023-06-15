from typing import Optional
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.forms import ValidationError
from django.http import HttpRequest
from django.utils import timezone


# Extending from Django's built-in user model.
# See: https://docs.djangoproject.com/en/4.2/ref/contrib/auth/#user-model
# See: https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#substituting-a-custom-user-model
# See: https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#specifying-a-custom-user-model


class UserManager(BaseUserManager):
  def create_user(self, username, password=None, **extra_fields):
    if not username:
      raise ValueError("The given username must be set.")
    user = self.model(username=username, **extra_fields)
    user.password = make_password(password)
    user.save()
    return user

  def create_superuser(self, username, password=None, **extra_fields):
    extra_fields.setdefault("admin", True)
    return self.create_user(username, password, **extra_fields)


def username_validator(username: str):
  if username.strip() != username:
    raise ValidationError('Username must not start with or end with a whitespace.')
  if len(username) < 4:
    raise ValidationError('Username must be at least 4 characters long.')


def user_directory_path(self: models.Model, filename: str) -> str:
  return 'accounts/user_{0}/{1}'.format(self.pk, filename)


class User(AbstractBaseUser):
  username = models.CharField(max_length=150, unique=True, validators=[username_validator])
  email = models.EmailField(blank=True)
  admin = models.BooleanField(default=False)
  avatar = models.ImageField(upload_to=user_directory_path, blank=True)
  first_name = models.CharField(max_length=150, blank=True)
  last_name = models.CharField(max_length=150, blank=True)
  bio = models.TextField(blank=True)
  date_joined = models.DateTimeField(default=timezone.now)
  # email_to_be_verified = models.EmailField(blank=True)
  # email_verification_token = models.BinaryField(max_length=128, blank=True)

  objects = UserManager()

  REQUIRED_FIELDS = []
  USERNAME_FIELD = 'username'
  EMAIL_FIELD = 'email'

  def __str__(self):
    return str(self.username)

  # The following properties are required by the Django administration site.

  @property
  def is_staff(self) -> bool:
    return self.admin

  @property
  def is_active(self) -> bool:
    return True

  def has_perm(self, perm: str, obj=None) -> bool:
    return self.admin

  def has_module_perms(self, app_label: str) -> bool:
    return self.admin


# Adding custom authentication backend, modified from Django's built-in ModelBackend
# https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#writing-an-authentication-backend
# https://github.com/django/django/blob/main/django/contrib/auth/backends.py

# This import must be put after the declaration of `class User`.
from django.contrib.auth.backends import BaseBackend  # nopep8


class AuthBackend(BaseBackend):
  def user_can_authenticate(self, user: User):
    return user.is_active

  def get_user(self, pk: int) -> Optional[User]:
    try:
      user = User.objects.get(pk=pk)
    except User.DoesNotExist:
      return None
    if not self.user_can_authenticate(user):
      return None
    return user

  def authenticate(
    self,
    request: HttpRequest,
    username: Optional[str] = None,
    password: Optional[str] = None,
    **kwargs
  ) -> Optional[User]:
    if username is None or password is None:
      return None
    try:
      user = User.objects.get(username=username)
    except User.DoesNotExist:
      User().check_password(password)
      return None
    if not user.check_password(password):
      return None
    if not self.user_can_authenticate(user):
      return None
    return user
