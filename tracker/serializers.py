from rest_framework import serializers
from tracker.models import *


class SetSerializer(serializers.ModelSerializer):
    """
    Additional fields to identify the User and the used equipment. Exercise_unit must be defined twice, since
    it's an not nullable field in the model (redefine for serializer).
    """
    exercise_unit = serializers.PrimaryKeyRelatedField(required=False, read_only=True, allow_null=True)
    equipment_id = serializers.CharField(write_only=True)
    exercise_name = serializers.CharField(write_only=True)
    rfid = serializers.CharField(write_only=True)

    class Meta:
        model = Set
        fields = ('id', 'date_time', 'exercise_unit', 'repetitions', 'weight', 'rfid', 'equipment_id', 'exercise_name')

    def validate(self, attrs):
        """
        Multiple validations of the input data coming from the client.
        """
        rfid_r = self.initial_data['rfid']
        exercise_unit_r = self.initial_data['exercise_unit']
        user_profile = UserProfile.objects.get(rfid_tag=rfid_r)
        equipment_id_r = self.initial_data['equipment_id']
        exercise_name_r = self.initial_data['exercise_name']

        # Check whether exercise_name and equipment fit:
        fit = False
        for exercise in Equipment.objects.get(id=equipment_id_r).exercises.all():
            if exercise.name == exercise_name_r:
                fit = True
                break
        if fit is False:
            raise ValidationError("Exercise name does not fit to Equipment-ID.")

        # TODO: move to create() method
        if exercise_unit_r == "None" or exercise_unit_r == "":
            # If there already exists a TrainUnit, update the end_time_date-field.
            if TrainUnit.objects.filter(date=timezone.now(), user=user_profile).exists():
                train_unit = TrainUnit.objects.get(date=timezone.now(), user=user_profile)
                train_unit.end_time_date = timezone.now()
            else:
                train_unit = TrainUnit.objects.create(date=timezone.now(), start_time_date=timezone.now(),
                                                      end_time_date=timezone.now(), user=user_profile)
            if train_unit.exercise_units.filter(exercise=Exercise.objects.get(name=exercise_name_r)).exists():
                exercise_unit = train_unit.exercise_units.get(exercise=Exercise.objects.get(name=exercise_name_r))
            else:
                exercise_unit = ExerciseUnit.objects.create(time_date=timezone.now(),
                                                        train_unit=train_unit,
                                                        exercise=Exercise.objects.get(name=exercise_name_r))
            attrs['exercise_unit'] = exercise_unit
            train_unit.exercise_units.add(exercise_unit)
            train_unit.save()
        return attrs

    def create(self, validated_data, **kwargs):
        """
        Remove additional parameters (rfid and exercise name) before creating the set-instance.
        """
        exercise_name = validated_data.pop('exercise_name')
        rfid = validated_data.pop('rfid')
        equipment_id = validated_data.pop('equipment_id')
        return Set.objects.create(**validated_data)

    def validate_equipment_id(self, value):
        """
        Check whether the provided exercise name exists.
        """
        if not Equipment.objects.filter(id=value).exists():
            raise serializers.ValidationError('Equipment-ID does not exist."')
        return value

    def validate_repetitions(self, value):
        """
        Logic test for repetitions:
         - not negative
         - not more than 499
        """
        if value <= 0:
            raise serializers.ValidationError('Repetitions must be greater than 0!')
        if value > 500:
            raise serializers.ValidationError('Too high value for repetitions.')
        return value

    def validate_weight(self, value):
        """
        Logic test for weight:
         - not negative
        """
        if value < 0:
            raise serializers.ValidationError('Weight must be positive!')
        return value

    def validate_rfid(self, value):
        """
        Test for rfid value:
         - length must be 10
        """
        if len(value) != 10:
            raise serializers.ValidationError('Not a valid RFID-Value!')
        return value
