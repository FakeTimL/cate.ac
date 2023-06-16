from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import serializers, views, permissions, status
from .models import *


# API endpoints that implement L-CRUD (list, create, retrieve, update, destory).
# See: https://www.django-rest-framework.org/api-guide/serializers/
# See: https://www.django-rest-framework.org/api-guide/views/
# See: https://www.django-rest-framework.org/api-guide/generic-views/
# See: https://www.django-rest-framework.org/api-guide/viewsets/


# Credential validator.
class CredentialSerializer(serializers.Serializer):
  username = serializers.CharField(max_length=150)
  password = serializers.CharField(max_length=128)


# Public view (read-only).
class UserBasicSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = [
      'pk', 'username',
      'avatar', 'first_name', 'last_name', 'bio',
      'date_joined', 'last_login',
    ]
    extra_kwargs = {
      'pk': {'read_only': True},
      'username': {'read_only': True},
      'avatar': {'read_only': True},
      'first_name': {'read_only': True},
      'last_name': {'read_only': True},
      'bio': {'read_only': True},
      'date_joined': {'read_only': True},
      'last_login': {'read_only': True},
    }


# Fields visible to self.
class UserSelfSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = [
      'pk', 'username', 'password', 'email',
      'avatar', 'first_name', 'last_name', 'bio',
      'date_joined', 'last_login',
    ]
    extra_kwargs = {
      'pk': {'read_only': True},
      'date_joined': {'read_only': True},
      'last_login': {'read_only': True},
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


class MessageSerializer(serializers.ModelSerializer):
  class Meta:
    model = Message
    fields = ['pk', 'sender', 'receiver', 'content', 'date']


class UsersView(views.APIView):
  # Disable DRF permission checking, use our own logic.
  permission_classes = [permissions.AllowAny]

  # List all users (staff only).
  def get(self, request: Request) -> Response:
    if not (isinstance(request.user, User) and request.user.admin):
      self.permission_denied(request)
    queryset = User.objects.order_by('pk')
    return Response(user_serializer(queryset, request=request, refl=False, many=True).data, status.HTTP_200_OK)

  # Create new user (i.e. sign up).
  def post(self, request: Request) -> Response:
    serializer = user_serializer(data=request.data, request=request, refl=True)
    serializer.is_valid(raise_exception=True)
    serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
    serializer.save()
    return Response(serializer.data, status.HTTP_201_CREATED)


class UserView(views.APIView):
  # Disable DRF permission checking, use our own logic.
  permission_classes = [permissions.AllowAny]

  # Retrieve user data.
  def get(self, request: Request, pk: int) -> Response:
    user = get_object_or_404(User, pk=pk)
    refl = isinstance(request.user, User) and request.user.pk == user.pk
    serializer = user_serializer(user, request=request, refl=refl)
    return Response(serializer.data, status.HTTP_200_OK)

  # Update user data.
  def put(self, request: Request, pk: int, partial=False) -> Response:
    user = get_object_or_404(User, pk=pk)
    refl = isinstance(request.user, User) and request.user.pk == user.pk
    serializer = user_serializer(user, request=request, refl=refl, data=request.data, partial=partial)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status.HTTP_200_OK)

  # Partially update user data.
  def patch(self, request: Request, pk: int) -> Response:
    return self.put(request, pk, partial=True)

  # Delete user (staff only).
  def delete(self, request: Request, pk: int) -> Response:
    if not (isinstance(request.user, User) and request.user.admin):
      self.permission_denied(request)
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return Response(None, status.HTTP_200_OK)


class SessionView(views.APIView):
  # Disable DRF permission checking, use our own logic.
  permission_classes = [permissions.AllowAny]

  # Retrieve currently active session (if exists).
  def get(self, request: Request) -> Response:
    if isinstance(request.user, User):
      serializer = user_serializer(request.user, request=request, refl=True)
      return Response(serializer.data, status.HTTP_200_OK)
    else:
      return Response(None, status.HTTP_200_OK)

  # Create new session (i.e. sign in).
  def post(self, request: Request):
    credentials = CredentialSerializer(data=request.data)
    credentials.is_valid(raise_exception=True)
    user = auth.authenticate(request, **credentials.validated_data)
    if user is None:
      return Response({'detail': 'Incorrect username or password.'}, status.HTTP_401_UNAUTHORIZED)
    auth.login(request, user)
    serializer = user_serializer(request.user, request=request, refl=True)
    return Response(serializer.data, status.HTTP_201_CREATED)

  # Delete session (i.e. sign out).
  def delete(self, request: Request) -> Response:
    auth.logout(request)
    return Response(None, status.HTTP_200_OK)


class MessagesView(views.APIView):
  # Disable DRF permission checking, use our own logic.
  permission_classes = [permissions.AllowAny]

  # List all messages from / to another user.
  def get(self, request: Request, pk: int) -> Response:
    if not isinstance(request.user, User):
      return Response(None, status.HTTP_200_OK)
    queryset_send = Message.objects.filter(sender=request.user.pk, receiver=pk)
    queryset_recv = Message.objects.filter(sender=pk, receiver=request.user.pk)
    queryset = queryset_send.union(queryset_recv).order_by('-date')
    return Response(MessageSerializer(queryset, many=True).data, status.HTTP_200_OK)

  # Create new message to a given user.
  def post(self, request: Request, pk: int) -> Response:
    if not isinstance(request.user, User):
      return Response(None, status.HTTP_200_OK)
    serializer = MessageSerializer(data={
      'sender': request.user.pk,
      'receiver': pk,
      'content': request.data.get('content'),
    })
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status.HTTP_201_CREATED)
