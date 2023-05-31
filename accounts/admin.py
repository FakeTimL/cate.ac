from django.contrib import admin

'''
from .models import User, Session

class UserAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {'fields': ['username', 'email']}),
    ('Additional information', {'fields': ['bio'], 'classes': ['collapse']})
  ]
  list_display = ['username', 'email', 'time_registered', 'email_verified']
  list_filter = ['time_registered']
  search_fields = ['username', 'email']

admin.site.register(User, UserAdmin)
'''

from .models import Profile

admin.site.register(Profile)
