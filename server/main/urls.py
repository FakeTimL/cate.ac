from django.urls import path
from . import views

app_name = 'main'  # Namespace for URLs
urlpatterns = [
  path('', views.topic_view, name='topic'),
  path('topic/', views.topic_view, name='topic'),
  path('topic/<int:id>/', views.topic_view, name='topic'),
  path('question/', views.question_view, name='question'),
  path('question/<int:id>/', views.question_view, name='question'),
  path('history/', views.history_view, name='history'),
  path('history/<int:id>/', views.history_view, name='history'),
  path('feedback/', views.feedback_view, name='feedback'),
]
