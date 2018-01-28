from rest_framework import serializers
from tracker.models import Set


class SetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Set
        fields = ('id', 'date_time', 'exercise_unit', 'repetitions', 'weight', 'rfid')

    """def create(self, validated_data):
        # exercise_unit = validated_data.pop('exercise_unit')
        obj = Set.objects.create(**validated_data)
        obj.save(exercise_unit=validated_data['exercise_unit'])
        return obj"""
