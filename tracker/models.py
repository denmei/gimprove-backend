from django.db import models
import uuid
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=False, blank=False)
    bio = models.TextField(max_length=500, blank=True, help_text="Beschreibung.")

    """@receiver(post_save, sender=User)
    def create_user_profile(self, sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(self, sender, instance, **kwargs):
        instance.profile.save()"""


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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise_units = models.ManyToManyField('ExerciseUnit', related_name='+', null=True, blank=True)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('training_unit', args=[str(self.id)])


class ExerciseUnit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    start_time_date = models.DateTimeField(null=False, blank=False)
    end_time_date = models.DateTimeField(null=False, blank=False)
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
