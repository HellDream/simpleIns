# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-14 11:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_userprofile_thumbs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='thumbs',
        ),
    ]