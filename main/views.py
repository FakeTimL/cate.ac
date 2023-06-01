from random import choice
from django.http import (Http404, HttpRequest, HttpResponse, HttpResponseNotFound,
                         HttpResponseRedirect, HttpResponseServerError)
from django.shortcuts import get_object_or_404
from django.template import loader
from django.urls import reverse
from django.contrib import messages
from markdown import Markdown
from pymdownx.arithmatex import ArithmatexExtension
from pymdownx.highlight import HighlightExtension
from .models import *


def object_not_found_view(request: HttpRequest, exception=None):
  return HttpResponseNotFound(loader.get_template('404.html').render({'reason': str(exception)}, request))


def internal_server_error_view(request: HttpRequest):
  return HttpResponseServerError(loader.get_template('500.html').render({}, request))


def feedback_view(request: HttpRequest):
  text = request.POST.get('content', '')
  if text != '':
    Feedback(text=text).save()
    messages.add_message(request, messages.SUCCESS, 'Your feedback has been sent!')
    return HttpResponseRedirect(reverse('main:feedback'))

  return HttpResponse(loader.get_template('main/feedback.html').render({
    'submit_url': reverse('main:feedback'),
    'submit_method': 'POST',
  }, request))


def question_view(request: HttpRequest, id=None):
  if id == None:
    try:
      id = choice(Question.objects.values_list('pk', flat=True))
    except IndexError:
      raise Http404('No question in database')

  question = get_object_or_404(Question, pk=id)

  user_answer = request.GET.get('answer_text', '')
  if user_answer != '':
    # TODO: send (user_answer + gpt_prompt) to GPT
    pass

  md = Markdown(extensions=[
    'nl2br',
    'smarty',
    'toc',
    'pymdownx.extra',
    'pymdownx.tilde',
    'pymdownx.mark',
    'pymdownx.escapeall',
    'pymdownx.tasklist',
    HighlightExtension(use_pygments=False),
    ArithmatexExtension(inline_syntax=['dollar'], block_syntax=['dollar'], smart_dollar=False, generic=True),
  ])
  question.statement = md.convert(question.statement)
  question.mark_scheme = md.convert(question.mark_scheme)

  return HttpResponse(loader.get_template('main/question.html').render({
    'question': question,
    'user_answer': user_answer,
    'submit_url': reverse('main:question', kwargs={'id': id}),
    'submit_method': 'GET',
  }, request))
