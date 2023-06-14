from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework import views, serializers, status, permissions
from .models import *


# API endpoints that implement L-CRUD (list, create, retrieve, update, destory).
# See: https://www.django-rest-framework.org/api-guide/serializers/
# See: https://www.django-rest-framework.org/api-guide/views/
# See: https://www.django-rest-framework.org/api-guide/generic-views/
# See: https://www.django-rest-framework.org/api-guide/viewsets/


# =======================
#     Users (public).
# =======================


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
      'username': {'read_only': True},
      'first_name': {'read_only': True},
      'last_name': {'read_only': True},
      'avatar': {'read_only': True},
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
      'superuser',
    ]


# Allow us to select a serializer based on `refl`.
# It is called `refl` since `self` cannot be used in Python.
def user_serializer(*args, request: Request, refl=False, **kwargs) -> serializers.BaseSerializer:
  if isinstance(request.user, User) and request.user.superuser:
    serializer_class = UserAdminSerializer
  elif refl:
    serializer_class = UserSelfSerializer
  else:
    serializer_class = UserBasicSerializer
  kwargs.setdefault('context', {'request': request})
  return serializer_class(*args, **kwargs)


class UsersView(views.APIView):
  permission_classes = [permissions.AllowAny]  # Disable DRF permission checking, use our own logic

  def get(self, request: Request) -> Response:
    queryset = User.objects.all().order_by('pk')
    return Response(user_serializer(queryset, request=request, refl=False, many=True).data, status.HTTP_200_OK)

  def post(self, request: Request) -> Response:
    serializer = user_serializer(data=request.data, request=request, refl=True)
    if serializer.is_valid():
      serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
      serializer.save()
      return Response(serializer.data, status.HTTP_201_CREATED)
    else:
      return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class UserView(views.APIView):
  permission_classes = [permissions.AllowAny]  # Disable DRF permission checking, use our own logic

  def get(self, request: Request, pk: int) -> Response:
    user = get_object_or_404(User, pk=pk)
    refl = isinstance(request.user, User) and request.user.pk == user.pk
    serializer = user_serializer(user, request=request, refl=refl)
    return Response(serializer.data, status.HTTP_200_OK)

  def put(self, request: Request, pk: int, partial=False) -> Response:
    user = get_object_or_404(User, pk=pk)
    refl = isinstance(request.user, User) and request.user.pk == user.pk
    serializer = user_serializer(user, request=request, refl=refl, data=request.data, partial=partial)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status.HTTP_200_OK)
    else:
      return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

  def patch(self, request: Request, pk: int) -> Response:
    return self.put(request, pk, partial=True)

  def delete(self, request: Request, pk: int) -> Response:
    # Only staffs can delete users.
    if isinstance(request.user, User) and request.user.superuser:
      user = get_object_or_404(User, pk=pk)
      user.delete()
      return Response(status.HTTP_204_NO_CONTENT)
    else:
      raise PermissionDenied


class CredentialSerializer(serializers.Serializer):
  username = serializers.CharField(max_length=150)
  password = serializers.CharField(max_length=128)


class SessionView(views.APIView):
  permission_classes = [permissions.AllowAny]  # Disable DRF permission checking, use our own logic

  def get(self, request: Request) -> Response:
    if isinstance(request.user, User):
      serializer = user_serializer(request.user, request=request, refl=True)
      return Response(serializer.data, status.HTTP_200_OK)
    else:
      return Response(status.HTTP_204_NO_CONTENT)

  def post(self, request: Request):
    serializer = CredentialSerializer(data=request.data)
    if serializer.is_valid():
      credential = serializer.validated_data
      user = auth.authenticate(request, username=credential['username'], password=credential['password'])
      if user is not None:
        auth.login(request, user)
        serializer = user_serializer(request.user, request=request, refl=True)
        return Response(serializer.data, status.HTTP_201_CREATED)
      else:
        raise PermissionDenied
    else:
      return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

  def delete(self, request: Request) -> Response:
    auth.logout(request)
    return Response(status.HTTP_204_NO_CONTENT)


# @login_required(redirect_field_name='redirect', login_url=reverse_lazy('accounts:login'))
# def me(request):
#   user = get_object_or_404(User, pk=request.user.id)
#   profile = get_object_or_404(Profile, user=request.user)

#   image_upload = request.FILES.get('image_upload', None)
#   if image_upload is not None:
#     filename = get_avatar_filename(request.user, image_upload)
#     if filename is None:
#       return HttpResponseRedirect(reverse('accounts:me'))
#     profile.avatar.save(filename, image_upload, save=True)  # Save file & update database
#     return HttpResponseRedirect(reverse('accounts:me'))

#   bio = request.POST.get('bio', None)
#   if bio is not None:
#     user.first_name = request.POST.get('first_name', '')
#     user.last_name = request.POST.get('last_name', '')
#     profile.bio = request.POST.get('bio', '')
#     user.save()
#     profile.save()
#     return HttpResponseRedirect(reverse('accounts:me'))

#   email = request.POST.get('email', None)
#   if email is not None:
#     # TODO: email verification
#     return HttpResponseRedirect(reverse('accounts:me'))

#   return render(request, 'accounts/me.html', {})
