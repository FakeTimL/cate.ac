from django.urls import path
from . import views

app_name = 'accounts'  # Namespace for URLs
urlpatterns = [
  path('users/', views.UsersView.as_view()),  # type: ignore
  path('user/<int:pk>/', views.UserView.as_view()),  # type: ignore
  path('me/', views.SessionView.as_view()),  # type: ignore
  path('me/conversations/', views.ConversationsView.as_view()),  # type: ignore
  path('me/conversation/<int:pk>/', views.ConversationView.as_view()),  # type: ignore
]
