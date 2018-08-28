from django.contrib import admin

from app_tracker.models.models import *


admin.site.register(TrainUnit)
admin.site.register(Exercise)
admin.site.register(ExerciseUnit)
admin.site.register(Set)
admin.site.register(Muscle)
admin.site.register(Equipment)
admin.site.register(UserTrackingProfile)
admin.site.register(MuscleGroup)