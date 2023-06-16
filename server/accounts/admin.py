# See: https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#custom-users-admin-full-example

from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.admin import ModelAdmin
from .models import *

admin.site.register(User, ModelAdmin)
admin.site.register(Message, ModelAdmin)
admin.site.unregister(Group)  # This is not needed anymore.
