# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.


class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager, self).filter(parent=None)
        return qs

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        object_id = instance.id
        queryset = super(CommentManager, self).filter(content_type=content_type, object_id=object_id).filter(parent=None)
        return queryset


class Comment(models.Model):
    user = models.ForeignKey(User, related_name="comment_user")
    content = models.CharField(max_length=512, default='')
    email = models.EmailField(null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = CommentManager()
    parent = models.ForeignKey("self", null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __unicode__(self):
        return str(self.user.username)

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True
