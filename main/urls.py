from django.urls import path
from . import views

app_name = 'main'  # Namespace for URLs
urlpatterns = [
  path('', views.question_view, name='question'),
  path('question/', views.question_view, name='question'),
  path('question/<int:id>/', views.question_view, name='question'),
  path('history/', views.history_view, name='history'),
  path('history/<int:id>/', views.history_view, name='history'),
  path('feedback/', views.feedback_view, name='feedback'),
  path('404/', views.object_not_found_view),
  path('500/', views.internal_server_error_view),
  # path('api/', views.api_view, name='api'),
]
