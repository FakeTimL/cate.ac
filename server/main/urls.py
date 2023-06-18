from django.urls import path
from . import views

app_name = 'main'  # Namespace for URLs
urlpatterns = [
  path('feedbacks/', views.FeedbacksView.as_view()),  # type: ignore
  path('feedback/<int:pk>/', views.FeedbackView.as_view()),  # type: ignore
  path('topics/', views.TopicsView.as_view()),  # type: ignore
  path('topic/<int:pk>/', views.TopicView.as_view()),  # type: ignore
  path('questions/', views.QuestionsView.as_view()),  # type: ignore
  path('question/<int:pk>/', views.QuestionView.as_view()),  # type: ignore
  path('sheets/', views.SheetsView.as_view()),  # type: ignore
  path('sheet/<int:pk>/', views.SheetView.as_view()),  # type: ignore
  path('submissions/', views.SubmissionsView.as_view()),  # type: ignore
  path('submission/<int:pk>/', views.SubmissionView.as_view()),  # type: ignore
  path('attempts/', views.AttemptsView.as_view()),  # type: ignore
  path('attempt/<int:pk>/', views.AttemptView.as_view()),  # type: ignore
  path('me/submissions/', views.UserSubmissionsView.as_view()),  # type: ignore
  path('me/submission/<int:pk>/', views.UserSubmissionView.as_view()),  # type: ignore
  path('question/<int:pk>/me/submissions/', views.UserQuestionSubmissionsView.as_view()),  # type: ignore
  path('me/attempts/', views.UserAttemptsView.as_view()),  # type: ignore
  path('me/attempt/<int:pk>/', views.UserAttemptView.as_view()),  # type: ignore
]
