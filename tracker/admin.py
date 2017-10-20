from django.contrib import admin

# Register your models here.

from .models import TrainUnit, Exercise, ExerciseUnit, Set, Muscle, Equipment, Profile

admin.site.register(TrainUnit)
admin.site.register(Exercise)
admin.site.register(ExerciseUnit)
admin.site.register(Set)
admin.site.register(Muscle)
admin.site.register(Equipment)
admin.site.register(Profile)
