from django.contrib import admin

# Register your models here.

from .models import User, TrainUnit, Exercise, ExerciseUnit, Set, Muscle

admin.site.register(User)
admin.site.register(TrainUnit)
admin.site.register(Exercise)
admin.site.register(ExerciseUnit)
admin.site.register(Set)
admin.site.register(Muscle)