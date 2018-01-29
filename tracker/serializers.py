from rest_framework import serializers
from tracker.models import *


class SetSerializer(serializers.ModelSerializer):
    # TODO: Zusätzliche Felder: RFID, Übungsname
    exercise_unit = serializers.PrimaryKeyRelatedField(required=False, read_only=True, allow_null=True)

    class Meta:
        model = Set
        fields = ('id', 'date_time', 'exercise_unit', 'repetitions', 'weight', 'rfid',)

    def validate(self, attrs):
        rfid_r = self.initial_data['rfid']
        exercise_unit_r = self.initial_data['exercise_unit']
        user_profile = UserProfile.objects.get(rfid_tag=rfid_r)
        if exercise_unit_r == "None" or exercise_unit_r == "":
            # If there already exists a TrainUnit, update the end_time_date-field.
            if TrainUnit.objects.filter(date=timezone.now(), user=user_profile).exists():
                train_unit = TrainUnit.objects.get(date=timezone.now(), user=user_profile)
                train_unit.end_time_date = timezone.now()
            else:
                train_unit = TrainUnit.objects.create(date=timezone.now(), start_time_date=timezone.now(),
                                                      end_time_date=timezone.now(), user=user_profile)
            if train_unit.exercise_units.filter(exercise=Exercise.objects.get(name="Lat Pulldown Machine")).exists():
                exercise_unit = train_unit.exercise_units.get(exercise=Exercise.objects.get(name="Lat Pulldown Machine"))
            else:
                exercise_unit = ExerciseUnit.objects.create(time_date=timezone.now(),
                                                        train_unit=train_unit,
                                                        exercise=Exercise.objects.get(name="Lat Pulldown Machine"))
            attrs['exercise_unit'] = exercise_unit
            train_unit.exercise_units.add(exercise_unit)
            train_unit.save()
        return attrs


    def validate_repetitions(self, value):
        if value < 0:
            raise serializers.ValidationError('Repetitions must be positive!')
        if value > 500:
            raise serializers.ValidationError('Too high value for repetitions.')
        return value


    def validate_weight(self, value):
        if value < 0:
            raise serializers.ValidationError('Weight must be positive!')
        return value

    def validate_rfid(self, value):
        if len(value) != 10:
            raise serializers.ValidationError('Not a valid RFID-Value!')
        return value
