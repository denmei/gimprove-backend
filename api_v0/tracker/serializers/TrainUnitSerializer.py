from rest_framework import serializers
from app_tracker.models.models import *


class TrainUnitSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrainUnit
        fields = '__all__'
