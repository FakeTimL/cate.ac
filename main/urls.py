from django.urls import path

from . import views
from django.views.generic import TemplateView

app_name = 'main' # namespace for urls
urlpatterns = [
  path('dev/design/', views.design_view, name='design'),
  path('dev/markdown_editor/', views.markdown_editor_view, name='markdown_editor'),
  path('dev/question_upload/', views.question_upload_view, name='question_upload'),
  path('dev/question_upload/convert/', views.question_upload_convert_view, name='question_upload_convert'),
  path('dev/question_upload/eval/', views.question_upload_eval_view, name='question_upload_eval'),
  
  path('', views.index_view, name='index'),
  path('about/', views.about_view, name='about'),
  path('help/', views.help_view, name='help'),
  path('feedback/', views.feedback_view, name='feedback'),
  path('api/', views.api_view, name='api'),
  path('infinideas_archive/', views.infinideas_archive_view, name='infinideas_archive'),
  path('acknowledgements/', views.acknowledgements_view, name='acknowledgements'),
  path('terms/', views.terms_of_use_view, name='terms_of_use'),
  path('privacy/', views.privacy_policy_view, name='privacy_policy'),
  
  path('comment/<int:comment_id>/', views.comment_view, name='comment'),
  path('search/', views.search_view, name='search'),
  
  path('courses/', views.courses_view, name='courses'),
  path('course/<slug:course_codename>/', views.course_view, name='course'),
  path('course/<slug:course_codename>/lecture/<int:lecture_id>/', views.lecture_view, name='lecture'),
  path('course/<slug:course_codename>/lecture/<int:lecture_id>/notes/', views.lecture_notes_view, name='lecture_notes'),
  
  #path('courses/manage/', views.manage_courses_view, name='manage_courses'),
  #path('course/<slug:course_codename>/edit/', views.edit_course_view, name='edit_course'),
  #path('course/<slug:course_codename>/lecture/<int:lecture_id>/edit/', views.edit_lecture_view, name='edit_lecture'),
  
  # Question request without AJAX:
  #  - View question in problemsets: GET question_view (args: [problemset,] question, [seed])
  #  - Answer question & view explanations in problemsets: GET question_view (args: [problemset,] question, seed; user_answer)
  # Customized queues, requires login:
  #  - View next question in queue: GET current_view (args: queue)
  #  - Answer question & view explanations in queue: POST current_view (args: queue; user_answer) => GET question_view (args: queue, question, seed; user_answer)
  
  # Individual questions
  path('problemsets/question/<int:question_id>/', views.question_view, name='question'),
  path('problemsets/question/<int:question_id>/<int:seed>/', views.question_view, name='question_with_seed'),
  
  # Questions in queues
  #path('problemsets/queues/', views.queues_view, name='queues'),
  #path('problemsets/queue/<int:queue_id>/', views.queue_view, name='queue'),
  path('problemsets/queue/<int:queue_id>/current/', views.current_view, name='current_question_in_queue'),
  path('problemsets/queue/<int:queue_id>/question/<int:question_id>/<int:seed>/', views.question_view, name='question_with_seed_in_queue'),
  
  # Questions in problemsets
  path('problemsets/', views.problemsets_view, name='problemsets'),
  path('problemset/<slug:problemset_codename>/', views.problemset_view, name='problemset'),
  path('problemset/<slug:problemset_codename>/question/<int:question_id>/', views.question_view, name='question_in_problemset'),
  path('problemset/<slug:problemset_codename>/question/<int:question_id>/<int:seed>/', views.question_view, name='question_with_seed_in_problemset'),
]
