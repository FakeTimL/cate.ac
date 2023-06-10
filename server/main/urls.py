from django.urls import path, re_path
from django.views.generic import TemplateView
from . import views

app_name = 'main'  # Namespace for URLs
urlpatterns = [
  path('api/', views.topic_view, name='topic'),
  path('api/topic/', views.topic_view, name='topic'),
  path('api/topic/<int:id>/', views.topic_view, name='topic'),
  path('api/question/', views.question_view, name='question'),
  path('api/question/<int:id>/', views.question_view, name='question'),
  path('api/history/', views.history_view, name='history'),
  path('api/history/<int:id>/', views.history_view, name='history'),
  path('api/feedback/', views.feedback_view, name='feedback'),
  path('api/404/', views.object_not_found_view),
  path('api/500/', views.internal_server_error_view),
  # All other URLs are routed to the frontend `index.html`
  re_path(r'', TemplateView.as_view(template_name='index.html'), name='index'),
]
