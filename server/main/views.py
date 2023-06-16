import logging
from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import serializers, views, generics, permissions, status
from markdown import Markdown
from pymdownx.arithmatex import ArithmatexExtension
from pymdownx.highlight import HighlightExtension
from .models import *
from .tasks import SubmissionThread

logger = logging.getLogger(__name__)


# API endpoints that implement L-CRUD (list, create, retrieve, update, destory).
# See: https://www.django-rest-framework.org/api-guide/serializers/
# See: https://www.django-rest-framework.org/api-guide/views/
# See: https://www.django-rest-framework.org/api-guide/generic-views/
# See: https://www.django-rest-framework.org/api-guide/viewsets/


class FeedbackSerializer(serializers.ModelSerializer):
  class Meta:
    model = Feedback
    fields = ['pk', 'text', 'email', 'date']
    extra_kwargs = {'date': {'read_only': True}}


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
    submission = Submission(
      user=user,
      question=question,
      user_answer=user_answer,
      gpt_mark=None,
      gpt_comments='',
    )
    submission.save()
    SubmissionThread(submission).start()  # This will trigger a request to ChatGPT.
    return Response(SubmissionSerializer(submission).data, status.HTTP_200_OK)


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
