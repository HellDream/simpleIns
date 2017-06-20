# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Comment
# Register your models here.


class CommentAdmin(admin.ModelAdmin):
    list_display = ['object_id', 'pk', 'content']
    list_display_links = ['pk']
    list_filter = ['content', 'object_id']

admin.site.register(Comment, CommentAdmin)
