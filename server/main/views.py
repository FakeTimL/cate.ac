import logging
import os
import json
from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import serializers, views, generics, permissions, status
import openai
import openai.error
from markdown import Markdown
from pymdownx.arithmatex import ArithmatexExtension
from pymdownx.highlight import HighlightExtension
from .models import *

logger = logging.getLogger(__name__)


# API endpoints that implement L-CRUD (list, create, retrieve, update, destory).
# See: https://www.django-rest-framework.org/api-guide/serializers/
# See: https://www.django-rest-framework.org/api-guide/views/
# See: https://www.django-rest-framework.org/api-guide/generic-views/
# See: https://www.django-rest-framework.org/api-guide/viewsets/


class FeedbackSerializer(serializers.ModelSerializer):
  class Meta:
    model = Feedback
    fields = ['pk', 'text', 'email', 'publish_date']
    extra_kwargs = {'publish_date': {'read_only': True}}


class TopicSerializer(serializers.ModelSerializer):
  children = serializers.PrimaryKeyRelatedField(many=True, queryset=Topic.objects)
  questions = serializers.PrimaryKeyRelatedField(many=True, queryset=Question.objects)

  class Meta:
    model = Topic
    fields = ['pk', 'name', 'parent', 'children', 'questions', 'resources']


class QuestionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Question
    fields = ['pk', 'statement', 'mark_denominator', 'mark_minimum',
              'mark_maximum', 'mark_scheme', 'gpt_prompt', 'topics']


class SubmissionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Submission
    fields = ['pk', 'user', 'question', 'user_answer', 'gpt_mark', 'gpt_comments', 'date']
    extra_kwargs = {'date': {'read_only': True}}


# This time we use DRF's abstractions for views (`GenericAPIView`) and permissions (`BasePermission`)
# since the requirement is simple enough (straightforward L-CRUD, staff writable, others readonly).

class IsAdmin(permissions.BasePermission):
  def has_permission(self, request: Request, view: views.APIView):
    return (isinstance(request.user, User) and request.user.admin)


class IsAdminOrReadOnly(permissions.BasePermission):
  def has_permission(self, request: Request, view: views.APIView):
    return (isinstance(request.user, User) and request.user.admin) or request.method in permissions.SAFE_METHODS


class IsAdminOrPostOnly(permissions.BasePermission):
  def has_permission(self, request: Request, view: views.APIView):
    return (isinstance(request.user, User) and request.user.admin) or request.method == 'POST'


class FeedbacksView(generics.ListCreateAPIView):
  queryset = Feedback.objects.order_by('pk')
  serializer_class = FeedbackSerializer
  permission_classes = [IsAdminOrPostOnly]


class FeedbackView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Feedback.objects
  serializer_class = FeedbackSerializer
  permission_classes = [IsAdminOrPostOnly]


class TopicsView(generics.ListCreateAPIView):
  queryset = Topic.objects.order_by('pk')
  serializer_class = TopicSerializer
  permission_classes = [IsAdminOrReadOnly]


class TopicView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Topic.objects
  serializer_class = TopicSerializer
  permission_classes = [IsAdminOrReadOnly]


class QuestionsView(generics.ListCreateAPIView):
  queryset = Question.objects.order_by('pk')
  serializer_class = QuestionSerializer
  permission_classes = [IsAdminOrReadOnly]


class QuestionView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Question.objects
  serializer_class = QuestionSerializer
  permission_classes = [IsAdminOrReadOnly]


class SubmissionsView(generics.ListCreateAPIView):
  queryset = Submission.objects.order_by('pk')
  serializer_class = SubmissionSerializer
  permission_classes = [IsAdmin]


class SubmissionView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Submission.objects
  serializer_class = SubmissionSerializer
  permission_classes = [IsAdmin]


class UserSubmissionsView(views.APIView):
  # Disable DRF permission checking, use our own logic.
  permission_classes = [permissions.AllowAny]

  # Retrieve all submissions for current user.
  def get(self, request: Request) -> Response:
    user = request.user
    if not isinstance(user, User):
      self.permission_denied(request)
    queryset = Submission.objects.filter(user=user).order_by('-date')
    return Response(SubmissionSerializer(queryset, many=True).data, status.HTTP_200_OK)


class UserQuestionSubmissionsView(views.APIView):
  # Disable DRF permission checking, use our own logic.
  permission_classes = [permissions.AllowAny]

  # Retrieve all submissions for current user and given question.
  def get(self, request: Request, pk: int) -> Response:
    question = get_object_or_404(Question, pk=pk)
    user = request.user
    if not isinstance(user, User):
      return Response([], status.HTTP_200_OK)
    queryset = Submission.objects.filter(user=user, question=question).order_by('-date')
    return Response(SubmissionSerializer(queryset, many=True).data, status.HTTP_200_OK)

  # Submit a new answer and have ChatGPT grade it.
  def post(self, request: Request, pk: int) -> Response:
    question = get_object_or_404(Question, pk=pk)
    user = request.user
    if not isinstance(user, User):
      user = None
    user_answer = request.data.get('user_answer', '(none)')
    try:
      (gpt_mark, gpt_comments) = gpt_invoke(question, user_answer)
      logger.info((request, user_answer, gpt_mark, gpt_comments))
      submission = Submission(
        user=user,
        question=question,
        user_answer=user_answer,
        gpt_mark=gpt_mark,
        gpt_comments=gpt_comments,
      )
      submission.save()
      return Response(SubmissionSerializer(submission).data, status.HTTP_200_OK)
    except json.JSONDecodeError as error:
      logger.warning(error)
      return Response({'detail': 'ChatGPT did not respond in valid JSON format.'}, status.HTTP_503_SERVICE_UNAVAILABLE)
    except ValueError as error:
      logger.warning(error)
      return Response({'detail': 'ChatGPT did not respond with a valid mark.'}, status.HTTP_503_SERVICE_UNAVAILABLE)
    except openai.error.RateLimitError as error:
      logger.warning(error)
      return Response({'detail': 'ChatGPT is too busy, please try again later...'}, status.HTTP_429_TOO_MANY_REQUESTS)
    except openai.error.OpenAIError as error:
      logger.warning(error)
      return Response({'detail': 'Unexpected ChatGPT error: ' + str(error)}, status.HTTP_503_SERVICE_UNAVAILABLE)


def gpt_invoke(question: Question, response: str) -> tuple[int, str]:
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
  content = completion.choices[0].message.content  # type: ignore
  feedback = json.loads(content)

  return int(float(feedback['mark']) * question.mark_denominator + 0.5), feedback['comment']


class MarkdownHTMLView(views.APIView):
  # Disable DRF permission checking, use our own logic.
  permission_classes = [permissions.AllowAny]

  # Convert Markdown to HTML.
  def post(self, request: Request) -> Response:
    markdown = request.data.get('markdown', '')
    return Response({'html': markdown_to_html(markdown)}, status.HTTP_200_OK)


def markdown_to_html(markdown: str) -> str:
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
