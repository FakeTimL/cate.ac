from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.templatetags.static import static

# Using Django's built-in user model
# https://docs.djangoproject.com/en/3.0/topics/auth/default/#user-objects
# https://docs.djangoproject.com/en/3.0/ref/contrib/auth/
# https://github.com/django/django/blob/master/django/contrib/auth/base_user.py
# https://github.com/django/django/blob/master/django/contrib/auth/models.py

User = get_user_model()


def user_directory_path(instance, filename):
  # File will be uploaded to MEDIA_ROOT/accounts/user_<id>/<filename>
  return 'accounts/user_{0}/{1}'.format(instance.user.id, filename)


class Profile(models.Model):
  ''' The profile table.
  '''
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  email_to_be_verified = models.EmailField(blank=True)
  email_verification_token = models.BinaryField(max_length=128, blank=True)
  avatar = models.ImageField(upload_to=user_directory_path, blank=True)
  bio = models.TextField(blank=True)

  def __str__(self):
    return str(self.user) + ": " + self.bio

  def get_avatar(self):
    return self.avatar.url if self.avatar else static('accounts/default_avatar.png')


# Adding custom authentication backend, modified from Django's built-in ModelBackend
# https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#writing-an-authentication-backend
# https://github.com/django/django/blob/master/django/contrib/auth/backends.py


class EmailAuthBackend(BaseBackend):
  ''' Additional authentication backend that checks input username against email address (so users can log in with email addresses)
  '''

  def authenticate(self, request, username=None, password=None):
    if username is None or password is None:
      return
    try:
      user = User._default_manager.get(email__iexact=username)
    except User.DoesNotExist:
      # Run the default password hasher once to reduce the timing
      # difference between an existing and a nonexistent user (#20760).
      User().set_password(password)
    else:
      if user.check_password(password) and self.user_can_authenticate(user):
        return user

  def user_can_authenticate(self, user):
    ''' Reject users with is_active = False. Custom user models that don't have that attribute are allowed.
    '''
    is_active = getattr(user, 'is_active', None)
    return is_active or is_active is None

  def get_user(self, user_id):
    try:
      user = User._default_manager.get(pk=user_id)
    except User.DoesNotExist:
      return None
    return user if self.user_can_authenticate(user) else None


def register(username, password, email=None):
  ''' Sign up procedure
  '''

  # 这玩意会把"！"变成"!", 还是不用了吧
  # username = UserModel.normalize_username(username) # Normalize visually identical Unicode characters

  try:
    user = User._default_manager.get_by_natural_key(username)
  except User.DoesNotExist:
    user = User._default_manager.create_user(username, email, password)
    Profile.objects.create(user=user)
    return user  # Success

  return None  # The same username have been registered
