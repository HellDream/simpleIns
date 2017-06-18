# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import UserProfile
# Register your models here.


class UserProfilModelAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user']
    list_filter = ['user']
    list_display_links = ['user', 'pk']

    class Meta:
        model = UserProfile

admin.site.register(UserProfile, UserProfilModelAdmin)
