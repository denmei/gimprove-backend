# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-22 16:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0009_auto_20171020_1623'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trainunit',
            name='exercice_units',
        ),
        migrations.AddField(
            model_name='trainunit',
            name='exercise_units',
            field=models.ManyToManyField(blank=True, null=True, related_name='_trainunit_exercise_units_+', to='tracker.ExerciseUnit'),
        ),
    ]