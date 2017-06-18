# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.
from posts.models import Post


class Comment(models.Model):
    user = models.ForeignKey(User, related_name="comment_user")
    post = models.ForeignKey(Post)
    content = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    email = models.EmailField()
