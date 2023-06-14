from django.urls import path
from . import views

app_name = 'main'  # Namespace for URLs
urlpatterns = [
  path('topics/', views.TopicsView.as_view(), name='topics'),
  path('topic/<int:pk>/', views.TopicView.as_view(), name='topic'),
  path('questions/', views.QuestionsView.as_view(), name='questions'),
  path('question/<int:pk>/', views.QuestionView.as_view(), name='question'),
  path('question/<int:question_pk>/submissions/', views.QuestionSubmissionsView.as_view(), name='question_submissions'),
  path('feedbacks/', views.FeedbacksView.as_view(), name='feedbacks'),
  path('feedback/<int:pk>/', views.FeedbackView.as_view(), name='feedback'),
]
