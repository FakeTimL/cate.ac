from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import *

admin.site.register(Feedback, ModelAdmin)
admin.site.register(Topic, ModelAdmin)
admin.site.register(Question, ModelAdmin)
admin.site.register(Submission, ModelAdmin)
