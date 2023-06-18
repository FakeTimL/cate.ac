from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import views, permissions, status
from .serializers import *


# API endpoints that implement L-CRUD (list, create, retrieve, update, destory).
# See: https://www.django-rest-framework.org/api-guide/serializers/
# See: https://www.django-rest-framework.org/api-guide/views/
# See: https://www.django-rest-framework.org/api-guide/generic-views/
# See: https://www.django-rest-framework.org/api-guide/viewsets/


class UsersView(views.APIView):
  permission_classes = [permissions.AllowAny]  # Disable DRF permission checking, use our own logic.

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
  permission_classes = [permissions.AllowAny]  # Disable DRF permission checking, use our own logic.

  # Retrieve user data.
  def get(self, request: Request, pk: int) -> Response:
    user = get_object_or_404(User, pk=pk)
    refl = isinstance(request.user, User) and request.user.pk == user.pk
    serializer = user_serializer(user, request=request, refl=refl)
    return Response(serializer.data, status.HTTP_200_OK)

  # Partially update user data.
  def patch(self, request: Request, pk: int) -> Response:
    user = get_object_or_404(User, pk=pk)
    refl = isinstance(request.user, User) and request.user.pk == user.pk
    serializer = user_serializer(user, request=request, refl=refl, data=request.data, partial=True)  # TODO
    serializer.initial_data['username'] = user.username
    serializer.is_valid(raise_exception=True)
    serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
    serializer.save()
    return Response(serializer.data, status.HTTP_200_OK)

  # Delete user (staff only).
  def delete(self, request: Request, pk: int) -> Response:
    if not (isinstance(request.user, User) and request.user.admin):
      self.permission_denied(request)
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return Response(None, status.HTTP_200_OK)


class SessionView(views.APIView):
  permission_classes = [permissions.AllowAny]  # Disable DRF permission checking, use our own logic.

  # Retrieve currently active session (if exists).
  def get(self, request: Request) -> Response:
    if not isinstance(request.user, User):
      return Response(None, status.HTTP_200_OK)
    serializer = user_serializer(request.user, request=request, refl=True)
    return Response(serializer.data, status.HTTP_200_OK)

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


class UserMessagesView(views.APIView):
  permission_classes = [permissions.AllowAny]  # Disable DRF permission checking, use our own logic.

  # List all messages.
  def get(self, request: Request) -> Response:
    if not isinstance(request.user, User):
      return Response(None, status.HTTP_200_OK)
    queryset_send = Message.objects.filter(sender=request.user.pk)
    queryset_recv = Message.objects.filter(receiver=request.user.pk)
    queryset = queryset_send.union(queryset_recv).order_by('-date')
    return Response(MessageSerializer(queryset, many=True).data, status.HTTP_200_OK)

  # Create new message to a given user.
  def post(self, request: Request) -> Response:
    if not isinstance(request.user, User):
      return Response(None, status.HTTP_200_OK)
    serializer = MessageSerializer(data=request.data)
    serializer.initial_data['sender'] = request.user.pk
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status.HTTP_201_CREATED)
