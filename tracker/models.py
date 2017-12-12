from django.db import models
import uuid
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
import os


# Create your models here.
def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.pk), filename)


class Connection(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)
    follower = models.ForeignKey(User, related_name="follower")
    followed = models.ForeignKey(User, related_name="followed")

    def __str__(self):
        return str(self.follower) + ":" + str(self.followed)


class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=False, blank=False)
    bio = models.TextField(max_length=500, blank=True, help_text="Beschreibung.")
    gym = models.ManyToManyField('Gym', blank=True)
    achievements = models.ManyToManyField('Achievement', blank=True)
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


class Exercise(models.Model):
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    time_date = models.DateTimeField(null=False, blank=False)
    train_unit = models.ForeignKey(TrainUnit, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class Set(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    date_time = models.DateTimeField(null=False, blank=False)
    exercise_unit = models.ForeignKey(ExerciseUnit, on_delete=models.CASCADE)
    repetitions = models.IntegerField()

    def __str__(self):
        return str(self.id)


class Equipment(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Gym(models.Model):
    name = models.CharField(max_length=100, help_text="Insert name of gym here.")
    members = models.ManyToManyField(User, blank=True)

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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    description = models.TextField(max_length=500, help_text="What kind of activity?", null=True,
                                   blank=True)

    def __str__(self):
        return str(self.user) + ": " + str(self.created)
