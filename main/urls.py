from django.urls import path
from . import views

app_name = 'main'  # Namespace for URLs
urlpatterns = [
  path('', views.question_view, name='question'),
  path('question/<int:id>/', views.question_view, name='question'),
  path('feedback/', views.feedback_view, name='feedback'),
  # path('api/', views.api_view, name='api'),
]
