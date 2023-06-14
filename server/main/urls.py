from django.urls import path
from . import views

app_name = 'main'  # Namespace for URLs
urlpatterns = [
  path('topics/', views.TopicsView.as_view(), name='topics'),
  path('topic/<int:pk>/', views.TopicView.as_view(), name='topic'),
  path('questions/', views.QuestionsView.as_view(), name='questions'),
  path('question/<int:pk>/', views.QuestionView.as_view(), name='question'),
  # path('histories/', views.HistoriesView.as_view(), name='histories'),
  # path('history/<int:pk>/', views.HistoryView.as_view(), name='history'),
  path('feedbacks/', views.FeedbacksView.as_view(), name='feedbacks'),
  path('feedback/<int:pk>/', views.FeedbackView.as_view(), name='feedback'),
]
