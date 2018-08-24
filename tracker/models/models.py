#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
import uuid
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
import os
from django.core.exceptions import ValidationError
from datetime import timedelta
import json
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.pk), filename)


class UserTrackingProfile(models.Model):
    user_profile = models.ForeignKey('main.UserProfile', on_delete=models.CASCADE)
    _pr_active_set = models.ForeignKey('tracker.Set', blank=True, null=True, on_delete=models.DO_NOTHING)

    @property
    def active_set(self):
        """
        Returns active set. If set has not been changed during the last 15 seconds, returns None.
        """
        if self._pr_active_set is not None:
            time_diff = timezone.now() - self._pr_active_set.last_update
            if time_diff.seconds > 15:
                self._pr_active_set = None
        return self._pr_active_set

    @active_set.setter
    def active_set(self, a_set):
        self._pr_active_set = a_set

    def __str__(self):
        return str(self.user_profile.user)

"""
class Connection(models.Model):
    
    Connection between a follower and the followed profile.
    
    created = models.DateTimeField(auto_now_add=True, editable=False)
    follower = models.ForeignKey(User, related_name="follower", on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name="followed", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.follower) + ":" + str(self.followed)

"""


class ClientConnection(models.Model):
    name = models.CharField(max_length=40, primary_key=True, blank=False, null=False)
    rfid_tag = models.CharField('RFID', max_length=10, blank=False, null=False)



class Exercise(models.Model):
    """
    Represents an executable exercise (not a group of sets!).
    """
    name = models.CharField(max_length=100, primary_key=True)
    description = models.CharField(max_length=1000, help_text="Insert short description here.")
    muscles = models.ManyToManyField('Muscle', help_text="Muscles trained by the exercise.")
    equipment_machine = models.ManyToManyField('Equipment', help_text="Necessary equipment for the exercise.", blank=True)
    gimprove_system = models.BooleanField(blank=False, null=False, default=False)
    # TODO: Auto-fill equipment machine when a new equipment for this exercise is created!

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('exercise-detail', args=[str(self.name)])



class MuscleGroup(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name


class Muscle(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    muscle_group = models.ForeignKey(MuscleGroup, on_delete=models.DO_NOTHING, null=False, blank=False)

    def __str__(self):
        return self.name


class TrainUnit(models.Model, LoginRequiredMixin):
    """
    Represents a group of exercise units executed together at a specific point of time.
    """
    login_url = '/login/'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    start_time_date = models.DateTimeField(default=timezone.now, null=False, blank=False)
    end_time_date = models.DateTimeField(default=timezone.now, null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    user = models.ForeignKey(UserTrackingProfile, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-start_time_date']

    def __str__(self):
        return str(timezone.localtime(self.start_time_date)) + " - " + str(timezone.localtime(self.end_time_date))

    def get_absolute_url(self):
        return reverse('exercise_unit_list', args=[str(self.id)])

    def clean(self):
        if self.start_time_date >= self.end_time_date:
            raise ValidationError('End time must be after start time!')


class Equipment(models.Model):
    """
    Represents a unique machine within a studio.
    """
    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    exercises = models.ManyToManyField(Exercise, blank=False)
    gym = models.ForeignKey('main.GymProfile', related_name="gym", on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.gym) + ": " + str(self.id)[0:5]


class ExerciseUnit(models.Model):
    """
    Represents a group of sets of the same exercise within the same TrainUnit.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    time_date = models.DateTimeField(default=timezone.now, null=False, blank=False)
    train_unit = models.ForeignKey(TrainUnit, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-time_date']

    def __str__(self):
        return str(self.exercise) + " " + str(timezone.localtime(self.time_date))

    def clean(self):
        if not ((self.time_date >= self.train_unit.start_time_date) and
                (self.time_date <= self.train_unit.end_time_date)):
            raise ValidationError("Time Date must be within End and Start time of TrainUnit.")


class Set(models.Model):
    """
    Represents a group of repetitions of the same exercise, directly executed one after the other.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    date_time = models.DateTimeField(default=timezone.now, null=False, blank=False)
    exercise_unit = models.ForeignKey(ExerciseUnit, on_delete=models.CASCADE)
    repetitions = models.IntegerField(blank=False)
    weight = models.FloatField(blank=False)
    durations = models.TextField(max_length=1200, blank=False, null=False)
    auto_tracking = models.BooleanField(blank=False, null=False, default=False)
    last_update = models.DateTimeField(default=timezone.now, null=False, blank=False)

    class Meta:
        ordering = ['-date_time']

    def __str__(self):
        return str(timezone.localtime(self.date_time)) + "_" + str(self.repetitions) + "r_" + str(self.id)[0:5]

    def clean(self):
        # check repetitions
        if (self.repetitions < 0) or (self.repetitions > 500):
            raise ValidationError("Not a reasonable value for repetitions.")
        # TODO check duration match repetition
        # check weight
        if self.weight < 0:
            raise ValidationError("No negative values allowed for weight.")
        # check whether set date fits the exercise unit date
        if not ((self.exercise_unit.time_date <= self.date_time) &
                (self.date_time <= (self.exercise_unit.time_date + timedelta(days=1)))):
            raise ValidationError("Date value does not fit to exercise unit.")
        # check whether number of durations and repetitions fit
        if len(json.loads(self.durations)) != self.repetitions:
            raise ValidationError("Number of durations values and repetitions do not fit.")

"""
class Achievement(models.Model):
    name = models.CharField(max_length=100, help_text="Insert the name of the achievement here.", primary_key=True)
    description = models.TextField(max_length=500, help_text="What did the user do to achieve it?", null=True,
                                   blank=True)
    user = models.ManyToManyField(User, blank=True)
    achievement_image = models.ImageField(upload_to=get_image_path, blank=True, null=True)

    def __str__(self):
        return str(self.name)


class Activity(models.Model):
    
    New training units, achievements etc. create activities that can be shared in the community.
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    description = models.TextField(max_length=500, help_text="What kind of activity?", null=True,
                                   blank=True)

    def __str__(self):
        return str(self.user) + ": " + str(self.created)
"""
