# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import string

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
import random

# Create your models here.
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify
from django.urls import reverse
from PIL import Image

from accounts.models import UserProfile


def upload_location(instance, filename):
    username = instance.user.username
    new_id = instance.id
    return "%s/%s/%s" %(username, new_id, filename)


class Post(models.Model):
    user = models.ForeignKey(User)
    photo = models.ImageField(upload_to=upload_location,
                              null=False,
                              width_field="width_field",
                              height_field="height_field"
                              )
    description = models.CharField(max_length=512, default='')
    likes = models.ManyToManyField(User,related_name="user_like",blank=True)
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    publish = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"slug": self.slug})

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

    def get_like_url(self):
        return reverse("posts:like-toggle", kwargs={"slug": self.slug})

    def get_user_image(self):
        image = UserProfile.objects.get(user=self.user).image.url
        return image

def random_string_generator(size):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance,new_slug=None):
    PostClass = instance.__class__
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(str(instance.user.username)+str("-")+str(instance.pk))
    qs_exists = PostClass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=5)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(pre_save_post_receiver, sender=Post)
