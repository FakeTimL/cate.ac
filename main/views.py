from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, JsonResponse, Http404, QueryDict
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.template import loader
from django.views.generic.base import TemplateView
from django.urls import reverse
from django.utils.http import urlencode
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType
from markdown2 import markdown
from elasticsearch_dsl import Search
from .models import *
import html, datetime, json
from .src.dynamic_question import init_dynamic_question, init_dynamic_question_from_json
from .src.spaced_repetition import update_question_schedule
from .src.anfaconv import anfa_convert
from django.utils.translation import gettext as _


# Convert dict to QueryDict
# https://stackoverflow.com/questions/13363628/django-can-i-create-a-querydict-from-a-dictionary
def dict_to_querydict(dictionary):
  from django.utils.datastructures import MultiValueDict
  qdict = QueryDict('', mutable=True)
  for key, value in dictionary.items():
    d = { key: value }
    qdict.update(MultiValueDict(d) if isinstance(value, list) else d)
  return qdict


# Django reverse with a querystring
# https://gist.github.com/benbacardi/227f924ec1d9bedd242b
def reverse_querystring(view, urlconf=None, args=None, kwargs=None, current_app=None, query_kwargs=None):
  base_url = reverse(view, urlconf=urlconf, args=args, kwargs=kwargs, current_app=current_app)
  if query_kwargs:
    query_dict = dict_to_querydict(query_kwargs)
    return '{}?{}'.format(base_url, urlencode(query_dict, doseq=True))
  return base_url


def index_view(request):
  '''
  template = loader.get_template('main/index.html')
  values = {}
  return HttpResponse(template.render(values, request))
  '''
  return render(request, 'main/index.html', {})


# More simple template views
def about_view(request):
  return render(request, 'main/text/about.html', {})
def help_view(request):
  return render(request, 'main/text/help.html', {})
def api_view(request):
  return render(request, 'main/text/api.html', {})
def infinideas_archive_view(request):
  return render(request, 'main/text/infinideas_archive.html', {
    'webpages': [
      {'name': _('Main page, version 3'), 'url': 'http://archive.anfatech.net/v3', 'year': '2015', 'description': _('Static page with hand-crafted CSS; responsive layout (by Zhanrong Qiao)'), 'image_static': 'main/infinideas_archive/v3.png'},
      {'name': _('NEWorld Forum'), 'url': 'http://archive.anfatech.net/NEWorld_Forum', 'year': '2015', 'description': _('Written in PHP + MySQL, with hand-crafted CSS (by Zhanrong Qiao & Shiyuan Yu)'), 'image_static': 'main/infinideas_archive/forum.png'},
      {'name': _('Main page, version 4'), 'url': 'http://archive.anfatech.net/', 'year': '2017', 'description': _('Written in PHP + MySQL, with hand-crafted CSS and a user account system (by Zhanrong Qiao). (There is also a description about the history of Infinideas...)'), 'image_static': 'main/infinideas_archive/v4.png'},
    ],
  })
def acknowledgements_view(request):
  return render(request, 'main/text/acknowledgements.html', {})
def terms_of_use_view(request):
  return render(request, 'main/text/terms_of_use.html', {})
def privacy_policy_view(request):
  return render(request, 'main/text/privacy_policy.html', {})


def feedback_view(request):
  if request.POST.get('content', '') != '':
    content = request.POST.get('content', '')
    new_feedback = Feedback.objects.create(text=content)
    messages.add_message(request, messages.SUCCESS, _('Your feedback has been sent!'))
    return HttpResponseRedirect(reverse('main:feedback'))
  
  return render(request, 'main/feedback.html', {})


def comment_view(request, comment_id):
  comment = get_object_or_404(Comment, pk=comment_id)
  
  if request.user.is_authenticated and request.POST.get('content', '') != '':
    content = request.POST.get('content', '')
    new_comment = Comment.objects.create(root=comment.root, parent=comment, user=request.user, text=content)
    return HttpResponseRedirect(request.POST.get('redirect_url', ''))
  
  if request.user.is_authenticated and request.POST.get('delete', '') == '1':
    if request.user == comment.user or request.user.is_staff:
      comment.delete()
      return HttpResponseRedirect(request.POST.get('redirect_url', ''))
    else:
      pass # TODO: return 403    
  
  children = Comment.objects.filter(parent=comment)
  all_comments = []
  for x in children:
    replies, has_more = list_subcomments(x.id)
    all_comments.append((x, replies, has_more))
  
  params = {
    'comment': comment,
    'all_comments': all_comments,
    'redirect_name': '',
    'redirect_url': '',
  }
  
  if comment.parent is not None:
    params['parent_id'] = comment.parent.id
  
  if comment.root.content_type.model_class() == Lecture:
    lecture = get_object_or_404(Lecture, pk=comment.root.object_id)
    params['redirect_name'] = _('lecture') # Return to what?
    params['redirect_url'] = reverse('main:lecture', args=(lecture.course.codename, lecture.id)) # Return to where?
  
  return render(request, 'main/comment.html', params)


def courses_view(request):
  all_courses = Course.objects.all()
  if not request.user.is_staff:
    all_courses = all_courses.filter(staff_only=False)
  
  return render(request, 'main/courses.html', {
    'all_courses': all_courses,
  })


def course_view(request, course_codename):
  course = get_object_or_404(Course, codename__iexact=course_codename)
  if not request.user.is_staff and course.staff_only:
    raise PermissionDenied(_("You are not allowed to view this course.")) # Triggers HTTP403
  
  all_lectures = Lecture.objects.filter(course=course.id)
  if not request.user.is_staff:
    all_lectures = all_lectures.filter(staff_only=False)
  
  return render(request, 'main/course.html', {
    'course': course,
    'all_lectures': all_lectures,
  })


def list_subcomments(comment_root_id, max_depth=4):
  ''' Returns tuple (replies, has_more)
  
  Set max_depth = -1 to allow arbitrary depth.
  '''
  children = Comment.objects.filter(parent=comment_root_id)
  
  if max_depth == 0:
    return [], len(children) > 0
  
  results = []
  for x in children:
    replies, has_more = list_subcomments(x.id, max_depth - 1)
    results.append((x, replies, has_more))
  
  return results, False


def lecture_view(request, course_codename, lecture_id):
  course = get_object_or_404(Course, codename__iexact=course_codename)
  all_lectures = Lecture.objects.filter(course=course.id)
  lecture = get_object_or_404(Lecture, pk=lecture_id, course__codename__iexact=course_codename)
  comment_root = get_comment_root_for(lecture)
  
  if not request.user.is_staff and (course.staff_only or lecture.staff_only):
    raise PermissionDenied(_("You are not allowed to view this lecture.")) # Triggers HTTP403
  
  if request.user.is_authenticated and request.POST.get('content', '') != '':
    content = request.POST.get('content', '')
    comment = Comment.objects.create(root=comment_root, user=request.user, text=content)
    return HttpResponseRedirect(reverse('main:lecture', args=(course_codename, lecture_id)))
  
  if lecture.lecture_notes is not None:
    lecture.lecture_notes = markdown(lecture.lecture_notes)
  else:
    lecture.lecture_notes = None
  
  children = Comment.objects.filter(root=comment_root).filter(parent=None)
  all_comments = []
  for x in children:
    replies, has_more = list_subcomments(x.id)
    all_comments.append((x, replies, has_more))
  
  return render(request, 'main/lecture.html', {
    'course': course,
    'all_lectures': all_lectures,
    'lecture': lecture,
    'all_comments': all_comments,
  })


def lecture_notes_view(request, course_codename, lecture_id):
  course = get_object_or_404(Course, codename__iexact=course_codename)
  lecture = get_object_or_404(Lecture, pk=lecture_id, course__codename__iexact=course_codename)
  
  if lecture.lecture_notes is not None:
    lecture.lecture_notes = markdown(lecture.lecture_notes)
  
  return render(request, 'main/lecture_notes.html', {
    'course': course,
    'lecture': lecture,
  })


def problemsets_view(request):
  all_problemsets = ProblemSet.objects.all()
  return render(request, 'main/problemsets.html', {
    'all_problemsets': all_problemsets,
  })


def problemset_view(request, problemset_codename):
  problemset = get_object_or_404(ProblemSet, codename__iexact=problemset_codename)
  all_questions = problemset.questions.all()
  return render(request, 'main/problemset.html', {
    'problemset': problemset,
    'all_questions': all_questions,
  })


def question_view(request, question_id, seed=None, queue_id=None, problemset_codename=None):
  ''' The view for questions. If the user has requested with GET, it also shows results & explanations.
  '''
  
  question_model = get_object_or_404(Question, pk=question_id)
  if problemset_codename is not None and not question_model.related_problemsets.filter(codename__iexact=problemset_codename).exists():
    raise Http404(_("Question not found in this problemset."))
  
  question = init_dynamic_question_from_json(question_model.data)
  user_responded = False
  
  if seed is not None:
    question.data['seed'] = int(seed)
    question.prepare()
    
    if True: #request.GET: # User has sent answer through GET
      user_responded = True
      answers = question.get_user_answers(request.GET)
      is_correct = question.validate_user_answers(answers)
      question.data['user_is_correct'] = is_correct
  else:
    question.prepare()
  
  submission_url = reverse('main:question_with_seed', args=(question_id, question.data['seed']))
  next_question_url = None
  back_url = reverse('main:problemsets')
  
  if queue_id is not None:
    next_question_url = reverse('main:current_question_in_queue', args=(queue_id,))
    #back_url =
  
  if problemset_codename is not None:
    submission_url = reverse('main:question_with_seed_in_problemset', args=(problemset_codename, question_id, question.data['seed']))
    back_url = reverse('main:problemset', args=(problemset_codename,))
  
  question.data['id'] = question_id
  return render(request, 'main/question.html', {
    'question_data': question.data,
    'user_responded': user_responded,
    'submission_method': 'get',
    'submission_url': submission_url,
    'next_question_url': next_question_url,
    'back_url': back_url,
  })


@login_required(redirect_field_name='redirect', login_url='/accounts/login')
def current_view(request, queue_id):
  ''' The view for the current question in the [main] queue
  '''
  
  all = QuestionSchedule.objects.filter(user_learning_data__user=request.user)
  fqs = all.order_by('time').first() # First question schedule
  
  now = timezone.now()
  if fqs is None or fqs.time > now:
    return render(request, 'main/queue_cleared.html', {
      'count_1hour': all.filter(time__lte=now+datetime.timedelta(hours=1)).count(),
      'count_3hours': all.filter(time__lte=now+datetime.timedelta(hours=3)).count(),
      'count_1day': all.filter(time__lte=now+datetime.timedelta(days=1)).count(),
      'count_7days': all.filter(time__lte=now+datetime.timedelta(days=7)).count(),
    })
  
  question_id, question_seed = fqs.question.id, fqs.seed # Decouple following logic with fqs (as it may be modified / deleted)
  question = init_dynamic_question_from_json(get_object_or_404(Question, pk=question_id).data)
  question.data['seed'] = question_seed
  
  if request.POST: # User responded
    answers = question.get_user_answers(request.POST)
    is_correct = question.validate_user_answers(answers)
    update_question_schedule(fqs, is_correct) # Update & save / delete fqs
    
    # Redirect
    return HttpResponseRedirect(reverse_querystring('main:question_with_seed_in_queue',
        args=(queue_id, question_id, question_seed,), query_kwargs=answers))
  
  question.prepare()
  question.data['id'] = question_id
  return render(request, 'main/question.html', {
    'question': question.data,
    'submission_method': 'post',
    'submission_url': reverse('main:current_question_in_queue', args=(queue_id,)),
  })


def search_view(request):
  assert False
  return # #####
  
  query = request.GET.get('query')
  es_results = []
  
  if query:
    search = Search(index=['lectures', 'courses', 'questions', 'problemsets'])
    es_results = search.query('multi_match', query=query, fields=['name', 'description', 'title', 'lecture_notes', 'data', 'source']).execute().hits
  
  results = []
  for es_result in es_results:
    results.append({
      'index': es_result.meta.index,
      'doc_type': es_result.meta.doc_type,
      'id': es_result.meta.id,
      'score': es_result.meta.score,
    })
  
  return render(request, 'main/search.html', {
    'query': query,
    'results': results,
    'total': es_results.total,
  })


# Administration views
# SECURITY NOTE: To ensure that only staff users can enter, add @user_passes_test(is_staff) before every funcion!

def is_staff(user):
  return user.is_staff;


@user_passes_test(is_staff, redirect_field_name='redirect', login_url='/accounts/login')
def design_view(request):
  fqs = QuestionSchedule.objects.filter(user_learning_data__user=request.user).order_by('time').first()
  
  return render(request, 'main/design.html', {
    'page_title': _('Anfa Learning - Design test'),
    'server_time': str(timezone.now()),
    'local_time': timezone.now(),
    'fqs_time': fqs.time,
    'request_get_host': request.get_host(),
  })


@user_passes_test(is_staff, redirect_field_name='redirect', login_url='/accounts/login')
def markdown_editor_view(request):
  if request.method == 'POST':
    return HttpResponse(markdown(request.body.decode('utf-8')))
  
  return render(request, 'main/markdown_editor.html', {
    'page_title': _('Anfa Learning'),
  })


@user_passes_test(is_staff, redirect_field_name='redirect', login_url='/accounts/login')
def question_upload_view(request):
  if request.method == 'POST':
    if request.POST.get('upload', '') == '1': # Form data, upload = True
      question_data_items = anfa_convert(request.POST.get('content', ''))
      num_questions = len(question_data_items)
      
      for item in question_data_items:
        q = Question(type=item['type'], data=json.dumps(item, ensure_ascii=False))
        q.save() # Insert into database
        LogEntry.objects.log_action(user_id=request.user.pk, content_type_id=ContentType.objects.get_for_model(q).pk, object_id=q.pk, object_repr=str(q), action_flag=ADDITION) # Log in admin site
      
      # For admin site URL reversal, see: https://docs.djangoproject.com/en/3.0/ref/contrib/admin/#admin-reverse-urls
      messages.add_message(request, messages.SUCCESS, _('Successfully added {0} questions. You may further edit or delete them in the <a href="{1}" target="_blank">administration page</a>.')
          .format(num_questions, reverse('admin:main_question_changelist')), extra_tags='safe')
      return HttpResponseRedirect(reverse('main:question_upload'))
  
  return render(request, 'main/question_upload.html', {
    'page_title': _('Anfa Learning'),
    'question_type_tags': Question.TYPE_CHOICES,
  })


@user_passes_test(is_staff, redirect_field_name='redirect', login_url='/accounts/login')
def question_upload_convert_view(request):
  if request.method == 'POST':
    # Wrap list inside a dict
    # See: https://stackoverflow.com/questions/25963552/json-response-list-with-django
    return JsonResponse({ 'wrapped_list': anfa_convert(request.body.decode('utf-8')) }) #ensure_ascii=False? # Returns JSON
  
  return HttpResponseBadRequest()


@user_passes_test(is_staff, redirect_field_name='redirect', login_url='/accounts/login')
def question_upload_eval_view(request):
  if request.method == 'POST':
    question = init_dynamic_question_from_json(request.body.decode('utf-8'))
    question.prepare()
    return JsonResponse(question.data) #ensure_ascii=False? # Returns JSON
  
  return HttpResponseBadRequest()

'''
@user_passes_test(is_staff, redirect_field_name='redirect', login_url='/accounts/login')
def manage_courses_view(request):
  return render(request, 'main/manage_courses.html', {})


@user_passes_test(is_staff, redirect_field_name='redirect', login_url='/accounts/login')
def edit_course_view(request, course_name):
  return render(request, 'main/edit_course.html', {
    'course_name': course_name,
  })


@user_passes_test(is_staff, redirect_field_name='redirect', login_url='/accounts/login')
def edit_lecture_view(request, course_name, lecture_id):
  return render(request, 'main/edit_lecture.html', {
    'course_name': course_name,
    'lecture_id': lecture_id,
  })
'''
