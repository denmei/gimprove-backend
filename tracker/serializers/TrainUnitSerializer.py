from rest_framework import serializers
from tracker.models.models import *


class TrainUnitSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrainUnit
        fields = '__all__'
