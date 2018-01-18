from django.db import models
import uuid
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse
import os


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
        connections = Connection.objects.filter(follower=self.user)
        follows = connections.values_list('followed', flat=True)
        return follows

    def get_activities(self):
        activities = Activity.objects.filter(user=self.user)
        return activities

    def get_follows_activities(self):
        activities = Activity.objects.filter().order_by('-created')
        return activities

    def __str__(self):
        return str(self.user)


class UserProfile(Profile):
    """
    Extended Profile for personal users (not Gyms).
    """
    date_of_birth = models.DateField(null=False, blank=False)
    gym = models.ManyToManyField('Gym', blank=True)
    achievements = models.ManyToManyField('Achievement', blank=True)


class GymProfile(Profile):
    """
    Extended Profile for gym users.
    """
    gym = models.OneToOneField('Gym', blank=False, on_delete=models.CASCADE)
    members = models.ManyToManyField('UserProfile', blank=True)


def get_profile_type(user):
    """
    Helps to determine whether the user has a user or a gym profile.
    :param user: Reference on user from request.
    :return: 'user' in case of UserProfile, 'gym' in case of GymProfile, 'None' else
    """
    if getattr(user.profile, 'userprofile'):
        return 'user'
    elif getattr(user.profile, 'gymprofile'):
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
    equipment = models.ManyToManyField('Equipment', help_text="Necessary equipment for the exercise.")

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise_units = models.ManyToManyField('ExerciseUnit', related_name='+', blank=True)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('exercise_unit_list', args=[str(self.id)])


class ExerciseUnit(models.Model):
    """
    Represents a group of sets of the same exercise within the same TrainUnit.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    time_date = models.DateTimeField(null=False, blank=False)
    train_unit = models.ForeignKey(TrainUnit, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class Set(models.Model):
    """
    Represents a group of repetitions of the same exercise, directly executed one after the other.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    date_time = models.DateTimeField(null=False, blank=False)
    exercise_unit = models.ForeignKey(ExerciseUnit, on_delete=models.CASCADE)
    repetitions = models.IntegerField()

    def __str__(self):
        return str(self.id)


class Equipment(models.Model):
    """
    Represents a unique machine within a studio.
    """
    # TODO Extend so equipment can be authenticated for uploading data
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


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
