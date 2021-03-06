# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-13 16:07
from __future__ import unicode_literals

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='height_field',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='width_field',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(height_field='height_field', upload_to=accounts.models.upload_location, width_field='width_field'),
        ),
    ]
