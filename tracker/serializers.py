from rest_framework import serializers
from tracker.models import Set


class SetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Set
        fields = ('id', 'date_time', 'exercise_unit', 'repetitions', 'weight')
