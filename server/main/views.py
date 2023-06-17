from datetime import datetime
import logging
from django.shortcuts import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import views, generics, permissions, status
from .serializers import *
from .tasks import *

logger = logging.getLogger(__name__)


# API endpoints that implement L-CRUD (list, create, retrieve, update, destory).
# See: https://www.django-rest-framework.org/api-guide/serializers/
# See: https://www.django-rest-framework.org/api-guide/views/
# See: https://www.django-rest-framework.org/api-guide/generic-views/
# See: https://www.django-rest-framework.org/api-guide/viewsets/


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


class SheetsView(generics.ListCreateAPIView):
  queryset = Sheet.objects.order_by('pk')
  serializer_class = SheetSerializer
  permission_classes = [IsAdminOrReadOnly]


class SheetView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Sheet.objects
  serializer_class = SheetSerializer
  permission_classes = [IsAdminOrReadOnly]


class SubmissionsView(generics.ListCreateAPIView):
  queryset = Submission.objects.order_by('pk')
  serializer_class = SubmissionSerializer
  permission_classes = [IsAdmin]  # Submissions should not be public.


class SubmissionView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Submission.objects
  serializer_class = SubmissionSerializer
  permission_classes = [IsAdmin]  # Submissions should not be public.


class AttemptsView(generics.ListCreateAPIView):
  queryset = Attempt.objects.order_by('pk')
  serializer_class = AttemptSerializer
  permission_classes = [IsAdmin]  # Attempts should not be public.


class AttemptView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Attempt.objects
  serializer_class = AttemptSerializer
  permission_classes = [IsAdmin]  # Attempts should not be public.


class UserSubmissionsView(views.APIView):
  permission_classes = [permissions.AllowAny]  # Disable DRF permission checking, use our own logic.

  # Retrieve all submissions for current user.
  def get(self, request: Request) -> Response:
    user = request.user
    if not isinstance(user, User):
      return Response([], status.HTTP_200_OK)
    queryset = Submission.objects.filter(user=user).order_by('-date')
    return Response(SubmissionSerializer(queryset, many=True).data, status.HTTP_200_OK)

  # Submit a new answer and have ChatGPT grade it.
  def post(self, request: Request) -> Response:
    user = request.user
    if not isinstance(user, User):
      self.permission_denied(request)
    serializer = SubmissionSerializer(data={
      'user': user.pk,
      'question': request.data.get('question'),
      'user_answer': request.data.get('user_answer'),
    })
    serializer.is_valid(raise_exception=True)
    submission = serializer.save()
    SubmissionsThread([submission]).start()  # This will trigger a request to ChatGPT.
    return Response(serializer.data, status.HTTP_201_CREATED)


class UserSubmissionView(views.APIView):
  permission_classes = [permissions.AllowAny]  # Disable DRF permission checking, use our own logic.

  # Retrieve a submission for current user.
  def get(self, request: Request, pk: int) -> Response:
    user = request.user
    submission = get_object_or_404(Submission, pk=pk)
    if not (isinstance(user, User) and user == submission.user):
      self.permission_denied(request)
    return Response(SubmissionSerializer(submission).data, status.HTTP_200_OK)

  # Delete submission.
  def delete(self, request: Request, pk: int) -> Response:
    user = request.user
    submission = get_object_or_404(Submission, pk=pk)
    if not (isinstance(user, User) and user == submission.user):
      self.permission_denied(request)
    submission.delete()
    return Response(None, status.HTTP_200_OK)


class UserQuestionSubmissionsView(views.APIView):
  permission_classes = [permissions.AllowAny]  # Disable DRF permission checking, use our own logic.

  # Retrieve all submissions for current user and given question.
  def get(self, request: Request, pk: int) -> Response:
    question = get_object_or_404(Question, pk=pk)
    user = request.user
    if not isinstance(user, User):
      return Response([], status.HTTP_200_OK)
    queryset = Submission.objects.filter(user=user, question=question).order_by('-date')
    return Response(SubmissionSerializer(queryset, many=True).data, status.HTTP_200_OK)


class UserAttemptsView(views.APIView):
  permission_classes = [permissions.AllowAny]  # Disable DRF permission checking, use our own logic.

  # Retrieve all attempts for current user.
  def get(self, request: Request) -> Response:
    user = request.user
    if not isinstance(user, User):
      return Response([], status.HTTP_200_OK)
    queryset = Attempt.objects.filter(user=user).order_by('-begin_time')
    return Response(AttemptSerializer(queryset, many=True).data, status.HTTP_200_OK)

  # Create a new attempt and record the start time.
  def post(self, request: Request) -> Response:
    user = request.user
    if not isinstance(user, User):
      self.permission_denied(request)
    serializer = AttemptSerializer(data=request.data)
    serializer.data['user'] = user.pk
    serializer.data['start_time'] = datetime.now()
    serializer.data['end_time'] = None
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status.HTTP_201_CREATED)


class UserAttemptView(views.APIView):
  permission_classes = [permissions.AllowAny]  # Disable DRF permission checking, use our own logic.

  # Retrieve an attempt for current user.
  def get(self, request: Request, pk: int) -> Response:
    user = request.user
    attempt = get_object_or_404(Attempt, pk=pk)
    if not (isinstance(user, User) and user == attempt.user):
      self.permission_denied(request)
    return Response(AttemptSerializer(attempt).data, status.HTTP_200_OK)

  # Partially update attempt data.
  def patch(self, request: Request, pk: int) -> Response:
    user = request.user
    attempt = get_object_or_404(Attempt, pk=pk)
    if not (isinstance(user, User) and user == attempt.user):
      self.permission_denied(request)
    if attempt.completed:
      self.permission_denied(request)

    just_completed = False
    serializer = AttemptSerializer(attempt)

    # Only allowed fields:
    if 'attempt_submissions' in request.data:
      serializer.data['attempt_submissions'] = request.data['attempt_submissions']
    if 'end_time' in request.data:
      serializer.data['end_time'] = datetime.now()
      just_completed = True

    serializer.is_valid(raise_exception=True)
    attempt = serializer.save()
    if just_completed:
      SubmissionsThread(list(attempt.submissions.all())).start()  # This will trigger requests to ChatGPT.
    return Response(serializer.data, status.HTTP_200_OK)

  # Delete attempt.
  def delete(self, request: Request, pk: int) -> Response:
    user = request.user
    attempt = get_object_or_404(Attempt, pk=pk)
    if not (isinstance(user, User) and user == attempt.user):
      self.permission_denied(request)
    attempt.delete()
    return Response(None, status.HTTP_200_OK)
