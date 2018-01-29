from rest_framework import serializers
from tracker.models import *


class SetSerializer(serializers.ModelSerializer):
    """
    Additional fields to identify the User and the used equipment. Exercise_unit must be defined twice, since
    it's an not nullable field in the model (redefine for serializer).
    """
    exercise_unit = serializers.PrimaryKeyRelatedField(required=False, read_only=True, allow_null=True)
    exercise_name = serializers.CharField(write_only=True)
    rfid = serializers.CharField(write_only=True)

    class Meta:
        model = Set
        fields = ('id', 'date_time', 'exercise_unit', 'repetitions', 'weight', 'rfid', 'exercise_name',)

    def validate(self, attrs):
        """
        Validation of exercise- and trainunit-options. If necessary, new units have to be created.
        """
        rfid_r = self.initial_data['rfid']
        exercise_unit_r = self.initial_data['exercise_unit']
        user_profile = UserProfile.objects.get(rfid_tag=rfid_r)
        exercise_name_r = self.initial_data['exercise_name']
        if exercise_unit_r == "None" or exercise_unit_r == "":
            # If there already exists a TrainUnit, update the end_time_date-field.
            if TrainUnit.objects.filter(date=timezone.now(), user=user_profile).exists():
                train_unit = TrainUnit.objects.get(date=timezone.now(), user=user_profile)
                train_unit.end_time_date = timezone.now()
            else:
                train_unit = TrainUnit.objects.create(date=timezone.now(), start_time_date=timezone.now(),
                                                      end_time_date=timezone.now(), user=user_profile)
            if train_unit.exercise_units.filter(exercise=Exercise.objects.get(name="Lat Pulldown Machine")).exists():
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
        return Set.objects.create(**validated_data)

    def validate_exercise_name(self, value):
        # TODO replace with Equipment-ID later.
        """
        Check whether the provided exercise name exists.
        """
        if not Exercise.objects.filter(name=value).exists():
            raise serializers.ValidationError('Exercise does not exist."')
        return value

    def validate_repetitions(self, value):
        """
        Logic test for repetitions:
         - not negative
         - not more than 499
        """
        if value < 0:
            raise serializers.ValidationError('Repetitions must be positive!')
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
