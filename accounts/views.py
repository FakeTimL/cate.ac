from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import register, UserModel, Profile
from unicodedata import category
from django.utils.translation import gettext as _
from django.utils import timezone

def index(request):
  '''
  template = loader.get_template('accounts/index.html')
  values = { ... }
  return HttpResponse(template.render(values, request))
  '''
  return render(request, 'accounts/index.html', {
    'page_title': _('Anfa Learning'),
  })


def login(request):
  error_message = None
  
  # Check if parameters are given
  username, password = request.POST.get('username', ''), request.POST.get('password', '')
  if username != '' and password != '':
    user = auth.authenticate(request, username=username, password=password) # Authenticate
    if user is not None: # Authentication successful
      auth.login(request, user) # Start session
      if request.POST.get('redirect', '') != '':
        return HttpResponseRedirect(request.POST['redirect']) # Redirect according to parameters
      return HttpResponseRedirect(reverse('accounts:index')) # Redirect to main page
    else:
      error_message = _('Invalid username or password')
  
  # Send login form
  return render(request, 'accounts/login.html', {
    'page_title': _('Log in'),
    'redirect': request.GET.get('redirect', ''),
    'error_message': error_message,
  })


def logout(request):
  auth.logout(request) # End session
  return HttpResponseRedirect(reverse('accounts:index')) # Redirect to main page


def sanitize_username(username):
  '''
  for c in username:
    if category(c)[0] == 'C':
      return False
  return True
  '''
  return True


def signup(request):
  error_message = None
  
  # Check if parameters are given
  username, password = request.POST.get('username', ''), request.POST.get('password', '')
  if username != '' and password != '':
    if sanitize_username(username):
      user = register(username, password, request.POST.get('email', None)) # Register
      if user is not None: # Registration successful
        auth.login(request, user) # Start session
        if request.POST.get('redirect', '') != '':
          return HttpResponseRedirect(request.POST['redirect']) # Redirect according to parameters
        return HttpResponseRedirect(reverse('accounts:index')) # Redirect to main page
      else:
        error_message = _('The same username have been registered. Please try another one.')
    else:
      error_message = _('The username must not contain Unicode control or formatting characters. Please try another one.')
  
  # Send signup form
  return render(request, 'accounts/signup.html', {
    'page_title': _('Sign up'),
    'redirect': request.GET.get('redirect', ''),
    'error_message': error_message,
  })


def get_avatar_filename(user, f): # Security check
  file_extension_allowlist =  ['.jpg', '.jpeg', '.png', '.gif', '.webp'] # Allowed image formats
  ext = ''
  for x in file_extension_allowlist:
    if f.name.endswith(x):
      ext = x
  if ext == '':
    return None
  return 'avatar' + ext


@login_required(redirect_field_name='redirect', login_url='/accounts/login') # `reverse('accounts:login')` will cause circular dependency during initialization
def me(request):
  image_upload = request.FILES.get('image_upload', None)
  if image_upload is not None:
    profile = get_object_or_404(Profile, user=request.user)
    filename = get_avatar_filename(request.user, image_upload)
    if filename is None:
      return HttpResponseRedirect(reverse('accounts:me')) # #####
    profile.avatar.save(filename, image_upload, save=True) # Save file & update database
    return HttpResponseRedirect(reverse('accounts:me'))
  
  bio = request.POST.get('bio', None)
  if bio is not None:
    user = get_object_or_404(UserModel, pk=request.user.id)
    profile = get_object_or_404(Profile, user=request.user)
    user.first_name, user.last_name, profile.bio = request.POST.get('first_name', ''), request.POST.get('last_name', ''), request.POST.get('bio', '')
    user.save()
    profile.save()
    return HttpResponseRedirect(reverse('accounts:me'))
  
  email = request.POST.get('email', None)
  if email is not None:
    user = get_object_or_404(UserModel, pk=request.user.id)
    profile = get_object_or_404(Profile, user=request.user)
    # Email verification start #####
    return HttpResponseRedirect(reverse('accounts:me'))
  
  return render(request, 'accounts/me.html', {
    'page_title': _('My profile'),
  })


def profile(request, username):
  user = get_object_or_404(UserModel, username__exact=username)
  return render(request, 'accounts/profile.html', {
    'u': user,
  })

