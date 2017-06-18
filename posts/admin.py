# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from posts.models import Post


class PostModelAdmin(admin.ModelAdmin):
    list_display = ['description', 'user', 'publish']
    list_display_links = ['publish']
    list_filter = ['description']
    class Meta:
        model = Post
# Register your models here.
admin.site.register(Post, PostModelAdmin)