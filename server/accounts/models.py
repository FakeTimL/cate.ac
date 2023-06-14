from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.utils import timezone


# Extending from Django's built-in user model.
# See: https://docs.djangoproject.com/en/4.2/ref/contrib/auth/#user-model
# See: https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#substituting-a-custom-user-model
# See: https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#specifying-a-custom-user-model


def user_directory_path(self: models.Model, filename: str) -> str:
  return 'accounts/user_{0}/{1}'.format(self.pk, filename)


class UserManager(BaseUserManager):
  def create_user(self, username, password=None, **extra_fields):
    if not username:
      raise ValueError("The given username must be set.")
    user = self.model(username=username, **extra_fields)
    user.password = make_password(password)
    user.save()
    return user

  def create_superuser(self, username, password=None, **extra_fields):
    extra_fields.setdefault("superuser", True)
    return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser):
  username = models.CharField(max_length=150, unique=True)
  email = models.EmailField(blank=True)
  superuser = models.BooleanField(default=False)
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


# Adding custom authentication backend, modified from Django's built-in ModelBackend
# https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#writing-an-authentication-backend
# https://github.com/django/django/blob/master/django/contrib/auth/backends.py

# class EmailAuthBackend(BaseBackend):
#   ''' Additional authentication backend that checks input username against email address (so users can log in with email addresses)
#   '''

#   def authenticate(self, request, username=None, password=None):
#     if username is None or password is None:
#       return
#     try:
#       user = User._default_manager.get(email__iexact=username)
#     except User.DoesNotExist:
#       # Run the default password hasher once to reduce the timing
#       # difference between an existing and a nonexistent user (#20760).
#       User().set_password(password)
#     else:
#       if user.check_password(password) and self.user_can_authenticate(user):
#         return user

#   def user_can_authenticate(self, user):
#     ''' Reject users with is_active = False. Custom user models that don't have that attribute are allowed.
#     '''
#     is_active = getattr(user, 'is_active', None)
#     return is_active or is_active is None

#   def get_user(self, user_id):
#     try:
#       user = User._default_manager.get(pk=user_id)
#     except User.DoesNotExist:
#       return None
#     return user if self.user_can_authenticate(user) else None
