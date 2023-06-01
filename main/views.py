import json
import os
from random import choice
from django.http import (Http404, HttpRequest, HttpResponse, HttpResponseNotFound,
                         HttpResponseRedirect, HttpResponseServerError)
from django.shortcuts import get_object_or_404
from django.template import loader
from django.urls import reverse
from django.contrib import messages
from markdown import Markdown
import openai
from pymdownx.arithmatex import ArithmatexExtension
from pymdownx.highlight import HighlightExtension
from .models import *


def object_not_found_view(request: HttpRequest, exception=None):
  return HttpResponseNotFound(loader.get_template('404.html').render({'reason': str(exception)}, request))


def internal_server_error_view(request: HttpRequest):
  return HttpResponseServerError(loader.get_template('500.html').render({}, request))


def prompt(question, criteria, response):
  instruction = 'You are an IB examiner. You should mark the student response carefully according to the question and marking criteria, and comment on how they may otherwise achieve full marks. Give your mark and comment in the following JSON format: {"mark":0,"comment":""}.'
  prompt = f"Question: {question}\n\nCriteria: {criteria}\n\nResponse: {response}"
  openai.api_key = os.environ['DRP49_OPENAI_API_KEY']
  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": instruction},
      {"role": "user", "content": prompt},
    ]
  )
  content = completion.choices[0].message.content
  feedback = json.loads(content)
  return feedback['mark'], feedback['comment']


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

  user_answer = request.GET.get('answer_text', None)
  (gpt_mark, gpt_comments) = (None, None)
  if user_answer is not None:
    (gpt_mark, gpt_comments) = prompt(question.statement, question.gpt_prompt, user_answer)
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
    'gpt_mark': gpt_mark,
    'gpt_comments': gpt_comments,
    'submit_url': reverse('main:question', kwargs={'id': id}),
    'submit_method': 'GET',
  }, request))
