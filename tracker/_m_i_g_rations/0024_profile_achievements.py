# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-26 17:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0023_achievement_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='achievements',
            field=models.ManyToManyField(blank=True, null=True, to='tracker.Achievement'),
        ),
    ]