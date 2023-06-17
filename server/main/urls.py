from django.urls import path
from . import views

app_name = 'main'  # Namespace for URLs
urlpatterns = [
  path('feedbacks/', views.FeedbacksView.as_view(), name='feedbacks'),  # type: ignore
  path('feedback/<int:pk>/', views.FeedbackView.as_view(), name='feedback'),  # type: ignore
  path('topics/', views.TopicsView.as_view(), name='topics'),  # type: ignore
  path('topic/<int:pk>/', views.TopicView.as_view(), name='topic'),  # type: ignore
  path('questions/', views.QuestionsView.as_view(), name='questions'),  # type: ignore
  path('question/<int:pk>/', views.QuestionView.as_view(), name='question'),  # type: ignore
  path('sheets/', views.SheetsView.as_view(), name='sheets'),  # type: ignore
  path('sheet/<int:pk>/', views.SheetView.as_view(), name='sheet'),  # type: ignore
  path('submissions/', views.SubmissionsView.as_view(), name='submissions'),  # type: ignore
  path('submission/<int:pk>/', views.SubmissionView.as_view(), name='submission'),  # type: ignore
  path('attempts/', views.AttemptsView.as_view(), name='attempts'),  # type: ignore
  path('attempt/<int:pk>/', views.AttemptView.as_view(), name='attempt'),  # type: ignore
  path('my_submissions/', views.UserSubmissionsView.as_view(), name='user_submissions'),  # type: ignore
  path('my_attempts/', views.UserAttemptsView.as_view(), name='user_attempts'),  # type: ignore
  path('question/<int:pk>/my_submissions/', views.UserQuestionSubmissionsView.as_view(),  # type: ignore
       name='user_question_submissions'),
]
