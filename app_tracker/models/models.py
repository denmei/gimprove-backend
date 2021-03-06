#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
import uuid
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta
import json
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from app_main.models.models import UserProfile
from django.db.models.signals import post_delete, pre_delete


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserTrackingProfile(models.Model):
    user_profile = models.ForeignKey('app_main.UserProfile', on_delete=models.CASCADE)
    _pr_active_set = models.ForeignKey('app_tracker.Set', blank=True, null=True, on_delete=models.DO_NOTHING)

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


class ClientConnection(models.Model):
    """
    Represents a connection from a client to the server. Created and used by the SetConsumer-Class for example.
    """
    name = models.CharField(max_length=40, primary_key=True, blank=False, null=False)
    user = models.CharField('user', max_length=10, blank=False, null=False)


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
    gym = models.ForeignKey('app_main.GymProfile', related_name="gym", on_delete=models.DO_NOTHING)

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
    exercise_unit = models.ForeignKey(ExerciseUnit, blank=True, null=True, on_delete=models.CASCADE, default=None)
    equipment = models.ForeignKey(Equipment, blank=True, null=True, on_delete=models.DO_NOTHING)
    exercise = models.ForeignKey(Exercise, blank=True, null=True, on_delete=models.CASCADE, default=None)
    repetitions = models.IntegerField(blank=False)
    weight = models.FloatField(blank=False)
    durations = models.TextField(max_length=1200, blank=False, null=False)
    auto_tracking = models.BooleanField(blank=False, null=False, default=False)
    rfid = models.CharField(max_length=10, blank=True, null=True, default=None)
    last_update = models.DateTimeField(default=timezone.now, null=False, blank=False)
    active = models.BooleanField(default=False, null=False, blank=False)

    class Meta:
        ordering = ['-date_time']

    def __str__(self):
        return str(timezone.localtime(self.date_time)) + "_" + str(self.repetitions) + "r_" + str(self.id)[0:5]

    def get_durations(self):
        return json.loads(self.durations)

    def clean(self):
        # Either at least exercisename & rfid or exerciseunit must be provided and valid
        if self.exercise_unit is None and (self.exercise is None or self.rfid is None):
            raise ValidationError("Either at least exercisename & rfid or exerciseunit must be provided")
        # check exerciseunit
        if self.exercise_unit is not None and len(ExerciseUnit.objects.filter(id=self.exercise_unit.id)) == 0:
            raise ValidationError("Not a valid exercise_unit")
        if self.exercise_unit is not None and ExerciseUnit.objects.get(id=self.exercise_unit.id).time_date > self.date_time:
            raise ValidationError("Set cannot have a date before it's exerciseunit")
        # check rfid
        if self.rfid is not None and len(UserProfile.objects.filter(rfid_tag=self.rfid)) == 0:
            raise ValidationError("Not a valid rfid")
        # check exercise
        if self.exercise is not None and len(Exercise.objects.filter(name=self.exercise.name)) == 0:
            raise ValidationError("Not a valid exercisename")
        # check repetitions
        if (self.repetitions < 0) or (self.repetitions > 500):
            raise ValidationError("Not a reasonable value for repetitions.")
        # check date: must be in the past
        if self.date_time > timezone.now():
            raise ValidationError("Date and time must be in the past.")
        # check weight
        if self.weight < 0:
            raise ValidationError("No negative values allowed for weight.")
        # check whether set date fits the exercise unit date
        if self.exercise_unit is not None:
            if not ((self.exercise_unit.time_date <= self.date_time) &
                    (self.date_time <= (self.exercise_unit.time_date + timedelta(days=1)))):
                raise ValidationError("Date value does not fit to exercise unit.")
        # check whether number of durations and repetitions fit
        if len(json.loads(self.durations)) != self.repetitions:
            raise ValidationError("Number of durations values and repetitions do not fit.")

    def save(self, *args, **kwargs):
        """
        Handles the creation of a new set.
        If there is no exerciseunit specified, check for a trainunit of the specified day first. If there is none,
        create a new trainunit and also a new exerciseunit within this new trainunit. Otherwise, check if there is
        a exerciseunit in the existing trainunit whose exercise matches the one of the set. If not, create a new one.
        Assign the set to the corresponding exerciseunit.
        """
        self.clean()

        # Create a new TrainUnit and ExerciseUnit if necessary.
        if self.exercise_unit is None:
            user_profile = UserProfile.objects.get(rfid_tag=self.rfid)
            user_tracking_profile = UserTrackingProfile.objects.get(user_profile=user_profile)
            # If there already exists a TrainUnit for this day, update the end_time_date-field.
            if TrainUnit.objects.filter(date=self.date_time, user=user_tracking_profile).exists():
                train_unit = TrainUnit.objects.get(date=self.date_time, user=user_tracking_profile)
                train_unit.end_time_date = self.date_time
            else:
                train_unit = TrainUnit.objects.create(date=self.date_time, start_time_date=self.date_time,
                                                      end_time_date=self.date_time, user=user_tracking_profile)
            #  check whether there already is a exercise unit for the specified exercise in the train unit
            if train_unit.exerciseunit_set.filter(exercise=Exercise.objects.get(name=self.exercise.name)).exists():
                exercise_unit_r = train_unit.exerciseunit_set.get(exercise=Exercise.objects.get(name=self.exercise.name))
            else:
                exercise_unit_r = ExerciseUnit.objects.create(time_date=self.date_time,
                                                              train_unit=train_unit,
                                                              exercise=Exercise.objects.get(name=self.exercise.name))
            self.exercise_unit = exercise_unit_r
        else:
            user_tracking_profile = self.exercise_unit.train_unit.user

        super(Set, self).save(*args, **kwargs)


@receiver(post_save, sender=Set)
def update_userprofile_active(sender, instance, **kwargs):
    if instance.active:
        user_tracking_profile = instance.exercise_unit.train_unit.user
        user_tracking_profile.active_set = instance
        user_tracking_profile.save()


@receiver(pre_delete, sender=Set)
def reset_userprofile_active(sender, instance, **kwargs):
    user_tracking_profile = instance.exercise_unit.train_unit.user
    if user_tracking_profile.active_set == instance:
        user_tracking_profile.active_set = None
        user_tracking_profile.save()


@receiver(post_delete, sender=Set)
def delete_empty_exercise_unit(sender, instance, **kwargs):
    """
    If a set is deleted and it's exercise_unit does not have any further sets, delete the exercise_unit.
    """
    exercise_unit = instance.exercise_unit
    if exercise_unit.set_set.count() < 1:
        exercise_unit.delete()


@receiver(post_delete, sender=ExerciseUnit)
def delete_empty_train_unit(sender, instance, **kwargs):
    """
    If an exercise_unit is deleted and it's train_unit does not have any further exercise_units, delete the train_unit.
    """
    train_unit = instance.train_unit
    if train_unit.exerciseunit_set.count() < 1:
        train_unit.delete()
