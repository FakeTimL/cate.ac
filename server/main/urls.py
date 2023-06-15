from django.urls import path
from . import views

app_name = 'main'  # Namespace for URLs
urlpatterns = [
  path('feedbacks/', views.FeedbacksView.as_view(), name='feedbacks'),
  path('feedback/<int:pk>/', views.FeedbackView.as_view(), name='feedback'),
  path('topics/', views.TopicsView.as_view(), name='topics'),
  path('topic/<int:pk>/', views.TopicView.as_view(), name='topic'),
  path('questions/', views.QuestionsView.as_view(), name='questions'),
  path('question/<int:pk>/', views.QuestionView.as_view(), name='question'),
  path('submissions/', views.SubmissionsView.as_view(), name='submissions'),
  path('submission/<int:pk>/', views.SubmissionView.as_view(), name='submission'),
  path('my_submissions/', views.UserSubmissionsView.as_view(), name='user_submissions'),
  path('question/<int:pk>/my_submissions/', views.UserQuestionSubmissionsView.as_view(), name='user_question_submissions'),
  path('markdown_html/', views.MarkdownHTMLView.as_view(), name='markdown_html'),
]
