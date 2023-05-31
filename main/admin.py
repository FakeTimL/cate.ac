from django.contrib import admin
from .models import *

class LectureAdmin(admin.ModelAdmin):
  exclude = ['comment_root']

class QuestionAdmin(admin.ModelAdmin):
  exclude = ['comment_root']

class ProblemSetAdmin(admin.ModelAdmin):
  exclude = ['comment_root']

class QuestionScheduleInline(admin.TabularInline):
  model = QuestionSchedule # Must have a foreign key relationship to UserLearningData
  extra = 1

class QuestionNotesInline(admin.TabularInline):
  model = QuestionNotes # Must have a foreign key relationship to UserLearningData
  extra = 1

class UserLearningDataAdmin(admin.ModelAdmin):
  inlines = [QuestionScheduleInline, QuestionNotesInline]

admin.site.register(Feedback)
#admin.site.register(CommentRoot)
admin.site.register(Comment)
admin.site.register(Course)
admin.site.register(Lecture, LectureAdmin)
admin.site.register(KnowledgeUnit)
admin.site.register(KnowledgeMap)
admin.site.register(Question, QuestionAdmin)
admin.site.register(ProblemSet, ProblemSetAdmin)
admin.site.register(UserLearningData, UserLearningDataAdmin)
