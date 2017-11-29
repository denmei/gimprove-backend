from django.contrib import admin

# Register your models here.

from .models import TrainUnit, Exercise, ExerciseUnit, Set, Muscle, Equipment, Profile, Gym, Achievement, Connection
from .models import Activity

admin.site.register(TrainUnit)
admin.site.register(Exercise)
admin.site.register(ExerciseUnit)
admin.site.register(Set)
admin.site.register(Muscle)
admin.site.register(Equipment)
admin.site.register(Profile)
admin.site.register(Gym)
admin.site.register(Achievement)
admin.site.register(Connection)
admin.site.register(Activity)
