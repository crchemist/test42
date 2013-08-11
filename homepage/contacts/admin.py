from __future__ import absolute_import

from django.contrib import admin

from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile, UserProfileAdmin)
