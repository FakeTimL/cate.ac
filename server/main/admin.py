from django.contrib import admin
from .models import *


# See: https://docs.djangoproject.com/en/4.2/ref/contrib/admin/#working-with-many-to-many-intermediary-models


class SheetQuestionInline(admin.StackedInline):
  model = SheetQuestion
  extra = 1


class SheetAdmin(admin.ModelAdmin):
  inlines = [SheetQuestionInline]


class AttemptSubmissionInline(admin.StackedInline):
  model = AttemptSubmission
  extra = 1


class AttemptAdmin(admin.ModelAdmin):
  inlines = [AttemptSubmissionInline]


admin.site.register(Feedback, admin.ModelAdmin)
admin.site.register(Topic, admin.ModelAdmin)
admin.site.register(Question, admin.ModelAdmin)
admin.site.register(Sheet, SheetAdmin)
admin.site.register(Submission, admin.ModelAdmin)
admin.site.register(Attempt, AttemptAdmin)
