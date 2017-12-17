# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-15 09:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0035_auto_20171129_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achievement',
            name='user',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='gym',
            name='members',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='achievements',
            field=models.ManyToManyField(blank=True, to='tracker.Achievement'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gym',
            field=models.ManyToManyField(blank=True, to='tracker.Gym'),
        ),
        migrations.AlterField(
            model_name='trainunit',
            name='exercise_units',
            field=models.ManyToManyField(blank=True, related_name='_trainunit_exercise_units_+', to='tracker.ExerciseUnit'),
        ),
    ]
