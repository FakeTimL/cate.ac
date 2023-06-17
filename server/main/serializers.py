from rest_framework import serializers
from .models import *


class FeedbackSerializer(serializers.ModelSerializer):
  class Meta:
    model = Feedback
    fields = ['pk', 'text', 'email', 'date']
    read_only_fields = ['pk', 'date']


class TopicSerializer(serializers.ModelSerializer):
  children = serializers.PrimaryKeyRelatedField(many=True, queryset=Topic.objects)
  questions = serializers.PrimaryKeyRelatedField(many=True, queryset=Question.objects)

  class Meta:
    model = Topic
    fields = ['pk', 'name', 'parent', 'children', 'questions', 'resources']
    read_only_fields = ['pk']


class QuestionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Question
    fields = ['pk', 'statement', 'mark_denominator', 'mark_minimum',
              'mark_maximum', 'mark_scheme', 'gpt_prompt', 'topics']
    read_only_fields = ['pk']


# See: https://stackoverflow.com/a/41996831
class SheetQuestionSerializer(serializers.ModelSerializer):
  class Meta:
    model = SheetQuestion
    fields = ['question', 'index']


class SheetSerializer(serializers.ModelSerializer):
  sheet_questions = SheetQuestionSerializer(source='sheetquestion_set', many=True)

  class Meta:
    model = Sheet
    fields = ['pk', 'user', 'sheet_questions', 'time_limit', 'name', 'description']
    read_only_fields = ['pk']


class SubmissionSerializer(serializers.ModelSerializer):
  class Meta:
    model = Submission
    fields = ['pk', 'user', 'question', 'user_answer', 'gpt_mark', 'gpt_comments', 'date']
    read_only_fields = ['pk', 'date']


class AttemptSerializer(serializers.ModelSerializer):
  class Meta:
    model = Attempt
    fields = ['pk', 'user', 'sheet', 'submissions', 'begin_time', 'end_time']
    read_only_fields = ['pk']
