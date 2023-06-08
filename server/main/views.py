import logging
import os
import json
from random import choice
from typing import Tuple
from django.http import (Http404, HttpRequest, HttpResponse, HttpResponseNotFound,
                         HttpResponseRedirect, HttpResponseServerError)
from django.shortcuts import get_object_or_404
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import openai
import openai.error
from markdown import Markdown
from pymdownx.arithmatex import ArithmatexExtension
from pymdownx.highlight import HighlightExtension
from .models import *

logger = logging.getLogger(__name__)


def object_not_found_view(request: HttpRequest, exception=None):
  return HttpResponseNotFound(loader.get_template('404.html').render({'reason': str(exception)}, request))


def internal_server_error_view(request: HttpRequest):
  return HttpResponseServerError(loader.get_template('500.html').render({}, request))


def topic_view(request: HttpRequest, id=None):
  if id == None:
    return HttpResponse(loader.get_template('main/topics.html').render({
      'topics': Topic.objects.all()
    }, request))

  return HttpResponse(loader.get_template('main/topic.html').render({
    'topic': get_object_or_404(Topic, pk=id)
  }, request))


def question_view(request: HttpRequest, id=None):
  if id == None:
    try:
      id = choice(Question.objects.values_list('pk', flat=True))
    except IndexError:
      raise Http404('No question in database')

  question = get_object_or_404(Question, pk=id)

  user_answer = request.POST.get('user_answer', None)
  (gpt_mark, gpt_comments) = (None, None)
  if user_answer is not None:
    try:
      (gpt_mark, gpt_comments) = gpt_invoke(question, user_answer)
      logger.info((request, user_answer, gpt_mark, gpt_comments))
      # Save history if user has logged in.
      if request.user.is_authenticated:
        history = History(
          user=request.user,
          question=question,
          user_answer=user_answer,
          gpt_mark=gpt_mark,
          gpt_comments=gpt_comments,
        )
        history.save()
        return HttpResponseRedirect(reverse('main:history', kwargs={'id': history.pk}))
    except json.JSONDecodeError as error:
      messages.add_message(request, messages.ERROR, 'ChatGPT did not respond in valid JSON format.')
      logger.warning(error)
    except ValueError as error:
      messages.add_message(request, messages.ERROR, 'ChatGPT did not respond with a valid mark.')
      logger.warning(error)
    except openai.error.RateLimitError as error:
      messages.add_message(request, messages.ERROR, 'ChatGPT is too busy, please try again later...')
      logger.warning(error)
    except openai.error.OpenAIError as error:
      messages.add_message(request, messages.ERROR, 'Unexpected ChatGPT error: ' + str(error))
      logger.warning(error)

  question.statement = convert_markdown(question.statement)
  question.mark_scheme = convert_markdown(question.mark_scheme)

  return HttpResponse(loader.get_template('main/question.html').render({
    'question': question,
    'user_answer': user_answer,
    'gpt_mark_divided': None if gpt_mark is None else gpt_mark / question.mark_denominator,
    'mark_maximum_divided': question.mark_maximum / question.mark_denominator,
    'gpt_comments': gpt_comments,
    'submit_url': reverse('main:question', kwargs={'id': id}),
    'submit_method': 'POST',
  }, request))


@login_required(redirect_field_name='redirect', login_url=reverse_lazy('accounts:login'))
def history_view(request: HttpRequest, id=None):
  if id == None:
    return HttpResponse(loader.get_template('main/histories.html').render({
      'histories': History.objects.filter(user=request.user)
    }, request))

  history = get_object_or_404(History, pk=id)
  history.question.statement = convert_markdown(history.question.statement)
  history.question.mark_scheme = convert_markdown(history.question.mark_scheme)
  gpt_mark_divided = format(history.gpt_mark / history.question.mark_denominator, '.0f')
  mark_maximum_divided = format(history.question.mark_maximum / history.question.mark_denominator, '.0f')

  return HttpResponse(loader.get_template('main/history.html').render({
    'history': history,
    'gpt_mark_displayed': f"{gpt_mark_divided} / {mark_maximum_divided}"
  }, request))


def feedback_view(request: HttpRequest):
  text = request.POST.get('content', '')
  if text != '':
    text = request.POST.get('email', '') + ': ' + text
    Feedback(text=text).save()
    messages.add_message(request, messages.SUCCESS, 'Your feedback has been sent!')
    return HttpResponseRedirect(reverse('main:feedback'))

  return HttpResponse(loader.get_template('main/feedback.html').render({
    'submit_url': reverse('main:feedback'),
    'submit_method': 'POST',
  }, request))


def convert_markdown(markdown: str) -> str:
  return Markdown(extensions=[
    'nl2br',
    'smarty',
    'toc',
    'pymdownx.extra',
    'pymdownx.tilde',
    'pymdownx.mark',
    'pymdownx.tasklist',
    'pymdownx.escapeall',
    HighlightExtension(use_pygments=False),
    ArithmatexExtension(inline_syntax=['dollar'], block_syntax=['dollar'], smart_dollar=False, generic=True),
  ]).convert(markdown)


def gpt_invoke(question: Question, response: str) -> Tuple[int, str]:
  openai.api_key = os.environ['DRP49_OPENAI_API_KEY']

  system = \
      'You are an IB examiner. You should mark the student response carefully according to the question and ' + \
      'marking criteria, and comment on how they may otherwise achieve full marks. Give your mark and comment ' + \
      'in the following JSON format: {"mark":0,"comment":""}. Make sure to respond in JSON only.\n' + \
      'Exam question:\n' + question.statement + '\n' + \
      'Marking criteria:\n' + question.gpt_prompt + '\n'
  user = 'The student\'s response:\n' + response + '\n'

  completion = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
      {'role': 'system', 'content': system},
      {'role': 'user', 'content': user},
    ]
  )
  content = completion.choices[0].message.content
  feedback = json.loads(content)

  return int(float(feedback['mark']) * question.mark_denominator + 0.5), feedback['comment']
