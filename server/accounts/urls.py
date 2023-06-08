from django.urls import path
# from django.contrib.auth import views as auth_views

from . import views

app_name = 'accounts'  # Namespace for URLs
urlpatterns = [
  path('', views.index, name='index'),
  path('login/', views.login, name='login'),
  path('logout/', views.logout, name='logout'),
  path('signup/', views.signup, name='signup'),
  path('me/', views.me, name='me'),
  path('profile/<str:username>/', views.profile, name='profile'),
]
