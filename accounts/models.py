# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import random
import string

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from PIL import Image
# Create your models here.
from django.urls import reverse
from django.utils.six import StringIO


def upload_location(instance, filename):
    username = instance.user.username
    pk = instance.pk
    chars = string.digits+string.ascii_letters
    new_filename = username+str("-")+str(pk).join(random.choice(chars) for _ in range(4))
    try:
        return "%s/%s/%s" %("profile", username,new_filename)
    except:
        return upload_location(instance, filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="user_profile")
    image = models.ImageField(upload_to=upload_location, width_field="width_field", height_field="height_field")
    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)
    signature = models.CharField(max_length=200, default="")

    def __unicode__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("accounts:profile", kwargs={"username": self.user.username})

