from rest_framework import serializers
from rest_framework import serializers
from app_tracker.models.models import *


class ExerciseUnitSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExerciseUnit
        fields = '__all__'
