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


# Create your models here.
def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.pk), filename)


class Connection(models.Model):
    """
    Connection between a follower and the followed profile.
    """
    created = models.DateTimeField(auto_now_add=True, editable=False)
    follower = models.ForeignKey(User, related_name="follower", on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name="followed", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.follower) + ":" + str(self.followed)


class Profile(models.Model):
    """
    Abstract class for the two user types - gyms and athletes (users). Attributes:
    """
    # TODO: Make abstract
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, help_text="Beschreibung.")
    profile_image = models.ImageField(upload_to=get_image_path, blank=True, null=True)

    def get_follows_connections(self):
        connections = Connection.objects.filter(follower=self.user)
        return connections

    def get_follower_connections(self):
        connections = Connection.objects.filter(followed=self.user)
        return connections

    def get_follow_ids(self):
        """
        :return: List of the ids of the Users the Profile is following.
        """
        connections = Connection.objects.filter(follower=self.user)
        follows = connections.values_list('followed', flat=True)
        return follows

    def get_activities(self):
        activities = Activity.objects.filter(user=self.user)
        return activities

    def get_follows_activities(self):
        activities = Activity.objects.filter().order_by('-created')
        return activities

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.user)


class UserProfile(Profile):
    """
    Extended Profile for personal users (not Gyms).
    """
    date_of_birth = models.DateField(null=False, blank=False)
    gym = models.ManyToManyField('GymProfile', blank=True)
    rfid_tag = models.CharField('RFID', max_length=10, blank=True, null=True)
    achievements = models.ManyToManyField('Achievement', blank=True)
    active_set = models.ForeignKey('Set', blank=True, null=True, on_delete=models.DO_NOTHING)


class GymProfile(Profile):
    """
    Extended Profile for gym users.
    """
    members = models.ManyToManyField('UserProfile', blank=True)


def get_profile_type(user):
    """
    Helps to determine whether the user has a user or a gym profile.
    :param user: Reference on user from request.
    :return: 'user' in case of UserProfile, 'gym' in case of GymProfile, 'None' else
    """
    if hasattr(user, 'userprofile'):
        return 'user'
    elif getattr(user, 'gymprofile'):
        return 'gym'
    else:
        return None


class Exercise(models.Model):
    """
    Represents an executable exercise (not a group of sets!).
    """
    name = models.CharField(max_length=100, primary_key=True)
    description = models.CharField(max_length=1000, help_text="Insert short description here.")
    muscles = models.ManyToManyField('Muscle', help_text="Muscles trained by the exercise.")
    equipment_machine = models.ManyToManyField('Equipment', help_text="Necessary equipment for the exercise.", blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('exercise-detail', args=[str(self.name)])


class Muscle(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name


class TrainUnit(models.Model, LoginRequiredMixin):
    """
    Represents a group of exercise units executed together at a specific point of time.
    """
    login_url = '/login/'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    start_time_date = models.DateTimeField(null=False, blank=False)
    end_time_date = models.DateTimeField(null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    exercise_units = models.ManyToManyField('ExerciseUnit', related_name='+', blank=True)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('exercise_unit_list', args=[str(self.id)])

    def clean(self):
        if self.start_time_date >= self.end_time_date:
            raise ValidationError('End time must be after start time!')


class ExerciseUnit(models.Model):
    """
    Represents a group of sets of the same exercise within the same TrainUnit.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    time_date = models.DateTimeField(null=False, blank=False)
    train_unit = models.ForeignKey(TrainUnit, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.exercise) + " " + str(self.time_date)

    def clean(self):
        if not (self.time_date >= self.train_unit.start_time_data and self.time_date <= self.train_unit.end_time_date):
            raise ValidationError("Time Date must be within End and Start time of TrainUnit.")


class Set(models.Model):
    """
    Represents a group of repetitions of the same exercise, directly executed one after the other.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    date_time = models.DateTimeField(default=timezone.now, null=False, blank=False)
    exercise_unit = models.ForeignKey(ExerciseUnit, on_delete=models.CASCADE)
    repetitions = models.IntegerField(blank=False)
    weight = models.IntegerField(blank=False)

    def __str__(self):
        return str(self.id)

    def clean(self):
        # check repetitions
        if self.repetitions < 0 or self.repetitions > 500:
            raise ValidationError("Not a reasonable value for repetitions.")
        # check weight
        if self.weight < 0:
            raise ValidationError("No negative values allowed for weight.")
        # check whether set date fits the exercise unit date
        if not (self.exercise_unit.time_date <= self.date_time <= self.exercise_unit.time_date + timedelta(days=1)):
            raise ValidationError("Date value does not fit to exercise unit.")


class Equipment(models.Model):
    """
    Represents a unique machine within a studio.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    exercises = models.ManyToManyField(Exercise, blank=False)
    gym = models.ForeignKey(GymProfile, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.gym) + ": " + str(self.id)[0:5]


class Achievement(models.Model):
    name = models.CharField(max_length=100, help_text="Insert the name of the achievement here.", primary_key=True)
    description = models.TextField(max_length=500, help_text="What did the user do to achieve it?", null=True,
                                   blank=True)
    user = models.ManyToManyField(User, blank=True)
    achievement_image = models.ImageField(upload_to=get_image_path, blank=True, null=True)

    def __str__(self):
        return str(self.name)


class Activity(models.Model):
    """
    New training units, achievements etc. create activities that can be shared in the community.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    description = models.TextField(max_length=500, help_text="What kind of activity?", null=True,
                                   blank=True)

    def __str__(self):
        return str(self.user) + ": " + str(self.created)
