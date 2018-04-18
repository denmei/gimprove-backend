from rest_framework import serializers
from rest_framework import serializers
from tracker.models.models import *


class ExerciseUnitSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExerciseUnit
