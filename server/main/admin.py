from django.contrib import admin
from .models import *

admin.site.register(Topic)
admin.site.register(Question)
admin.site.register(History)
admin.site.register(Feedback)
