# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-26 18:05
from __future__ import unicode_literals

from django.db import migrations, models
import tracker.models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0025_auto_20171126_1754'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to=tracker.models.get_image_path),
        ),
    ]
