from django.urls import path
from . import views

app_name = 'accounts'  # Namespace for URLs
urlpatterns = [
  path('users/', views.UsersView.as_view(), name='users'),  # type: ignore
  path('user/<int:pk>/', views.UserView.as_view(), name='user'),  # type: ignore
  path('session/', views.SessionView.as_view(), name='session'),  # type: ignore
]
