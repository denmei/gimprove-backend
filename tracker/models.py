from django.db import models
import uuid
from django.urls import reverse

# Create your models here.


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_lenght=30)
    date_of_birth = models.DateField(null=False, blank=False)
    train_units = models.ManyToManyField(TrainUnit)

    class Meta:
        ordering = ('last_name', 'first_name', 'date_of_birth',)

    def get_absolute_url(self):
        return reverse('user-detail', args=[str(self.id)])

    def __str__(self):
        return self.id


class Exercise(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    description = models.CharField(max_length=1000, help_text="Insert short description here.")
    muscles = models.ManyToManyField(Muscle, help_text="Muscles trained by the exercise.")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('exercise-detail', args=[str(self.name)])


class Muscle(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name


class TrainUnit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    start_time_date = models.DateTimeField(null=False, blank=False)
    end_time_date = models.DateTimeField(null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.id


class ExerciseUnit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    start_time_date = models.DateTimeField(null=False, blank=False)
    end_time_date = models.DateTimeField(null=False, blank=False)
    train_unit = models.ForeignKey(TrainUnit, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

    def __str__(self):
        return self.id


class Set(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    date_time = models.DateTimeField(null=False, blank=False)
    exercise_unit = models.ForeignKey(ExerciseUnit, on_delete=models.CASCADE)
    repetitions = models.IntegerField()

    def __str__(self):
        return self.id