from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from .models import register, User, Profile


def index(request):
  return render(request, 'accounts/index.html')


def login(request):
  error_message = None

  # Check if parameters are given
  username, password = request.POST.get('username', ''), request.POST.get('password', '')
  if username != '' and password != '':
    user = auth.authenticate(request, username=username, password=password)  # Authenticate
    if user is not None:  # Authentication successful
      auth.login(request, user)  # Start session
      if request.POST.get('redirect', '') != '':
        return HttpResponseRedirect(request.POST['redirect'])  # Redirect according to parameters
      return HttpResponseRedirect(reverse('accounts:index'))  # Redirect to main page
    else:
      error_message = 'Invalid username or password'

  # Send login form
  return render(request, 'accounts/login.html', {
    'redirect': request.GET.get('redirect', ''),
    'error_message': error_message,
  })


def logout(request):
  auth.logout(request)  # End session
  return HttpResponseRedirect(reverse('accounts:index'))  # Redirect to main page


def signup(request):
  error_message = None

  username = request.POST.get('username', '')
  password = request.POST.get('password', '')
  email = request.POST.get('email', None)

  # Check if parameters are given
  if username != '' and password != '':
    user = register(username, password, email)  # Register
    if user is not None:  # Registration successful
      auth.login(request, user)  # Start session
      messages.add_message(request, messages.SUCCESS, 'User account created!')
      return HttpResponseRedirect(request.POST.get('redirect', reverse('accounts:index')))
    else:
      error_message = 'The same username have been registered. Please try another one.'

  # Send signup form
  return render(request, 'accounts/signup.html', {
    'redirect': request.GET.get('redirect', ''),
    'error_message': error_message,
  })


def get_avatar_filename(user, f):
  file_extension_allowlist = ['.jpg', '.jpeg', '.png', '.gif', '.webp']  # Allowed image formats
  ext = ''
  for x in file_extension_allowlist:
    if f.name.endswith(x):
      ext = x
  if ext == '':
    return None
  return 'avatar' + ext


@login_required(redirect_field_name='redirect', login_url=reverse_lazy('accounts:login'))
def me(request):
  user = get_object_or_404(User, pk=request.user.id)
  profile = get_object_or_404(Profile, user=request.user)

  image_upload = request.FILES.get('image_upload', None)
  if image_upload is not None:
    filename = get_avatar_filename(request.user, image_upload)
    if filename is None:
      return HttpResponseRedirect(reverse('accounts:me'))
    profile.avatar.save(filename, image_upload, save=True)  # Save file & update database
    return HttpResponseRedirect(reverse('accounts:me'))

  bio = request.POST.get('bio', None)
  if bio is not None:
    user.first_name = request.POST.get('first_name', '')
    user.last_name = request.POST.get('last_name', '')
    profile.bio = request.POST.get('bio', '')
    user.save()
    profile.save()
    return HttpResponseRedirect(reverse('accounts:me'))

  email = request.POST.get('email', None)
  if email is not None:
    # TODO: email verification
    return HttpResponseRedirect(reverse('accounts:me'))

  return render(request, 'accounts/me.html', {})


def profile(request, username):
  user = get_object_or_404(User, username__exact=username)
  return render(request, 'accounts/profile.html', {'user': user})
