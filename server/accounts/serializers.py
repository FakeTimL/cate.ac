from rest_framework import serializers
from rest_framework.request import Request
from .models import *


# Public view (read-only).
class UserBasicSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = [
      'pk', 'username',
      'avatar', 'first_name', 'last_name', 'bio',
      'date_joined', 'last_login',
      'admin',
    ]
    read_only_fields = [
      'pk', 'username',
      'avatar', 'first_name', 'last_name', 'bio',
      'date_joined', 'last_login',
      'admin',
    ]


# Fields visible to self.
class UserSelfSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = [
      'pk', 'username', 'password', 'email',
      'avatar', 'first_name', 'last_name', 'bio',
      'date_joined', 'last_login',
      'admin',
    ]
    read_only_fields = [
      'pk',
      'date_joined', 'last_login',
      'admin',
    ]
    extra_kwargs = {
      'password': {'write_only': True},
    }


# All fields.
class UserAdminSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = [
      'pk', 'username', 'password', 'email',
      'avatar', 'first_name', 'last_name', 'bio',
      'date_joined', 'last_login',
      'admin',
    ]


# Allow us to select a serializer based on `refl`.
# It is called `refl` since `self` cannot be used in Python.
def user_serializer(*args, request: Request, refl=False, **kwargs) -> serializers.BaseSerializer:
  if isinstance(request.user, User) and request.user.admin:
    return UserAdminSerializer(*args, **kwargs)
  elif refl:
    return UserSelfSerializer(*args, **kwargs)
  else:
    return UserBasicSerializer(*args, **kwargs)


# Credential validator.
class CredentialSerializer(serializers.Serializer):
  username = serializers.CharField(max_length=150)
  password = serializers.CharField(max_length=128)


class MessageSerializer(serializers.ModelSerializer):
  class Meta:
    model = Message
    fields = ['pk', 'sender', 'receiver', 'content', 'date']
    read_only_fields = ['pk', 'date']
