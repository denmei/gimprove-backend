import json

from rest_framework import serializers

from tracker.models.models import *

"""
These serializers may only be used by authenticated components since they provide extra functionalities.
"""
# TODO: Add permission to restrict access only to authenticated equipment components
# TODO: Extra mark for sets that were tracked by equipment components
# TODO: Disable delete and get_list functionality since not needed by equipment components


class SetSerializer(serializers.ModelSerializer):
    """
    Additional fields to identify the User and the used equipment. Exercise_unit must be defined twice, since
    it's an not nullable field in the model (redefine for serializer).
    """
    exercise_unit = serializers.PrimaryKeyRelatedField(required=False, read_only=True, allow_null=True)
    equipment_id = serializers.CharField(write_only=True)
    exercise_name = serializers.CharField(write_only=True)
    active = serializers.CharField(write_only=True)
    rfid = serializers.CharField(write_only=True)

    class Meta:
        model = Set
        fields = ('id', 'date_time', 'durations', 'exercise_unit', 'repetitions', 'weight', 'rfid', 'equipment_id',
                  'exercise_name', 'active')

    def validate(self, attrs):
        """
        Multiple validations of the input data coming from the client.
        """
        # TODO: Check whether all values in request
        # TODO: check durations vs. repetitions
        equipment_id_r = self.initial_data['equipment_id']
        exercise_name_r = self.initial_data['exercise_name']
        durations = self.initial_data['durations']
        repetitions = self.initial_data['repetitions']

        # Check whether exercise_name and equipment fit:
        fit = False
        for exercise in Equipment.objects.get(id=equipment_id_r).exercises.all():
            if exercise.name == exercise_name_r:
                fit = True
                break
        if fit is False:
            raise ValidationError("Exercise name does not fit to Equipment-ID.")

        # check whether duration values and repetitions fit
        durations = json.loads(durations)
        if len(durations) != int(repetitions):
            raise ValidationError("The number of duration values must be equal to the number of repetitions." +
                                  str(len(durations)) + " " + str(durations) + " " + str(repetitions))

        return self.initial_data

    def create(self, validated_data, **kwargs):
        """
        Remove additional parameters (rfid and exercise name) before creating the set-instance.
        """
        # Pop the data not needed to create a set.
        exercise_name_r = validated_data.pop('exercise_name')
        rfid_r = validated_data.pop('rfid')
        equipment_id = validated_data.pop('equipment_id')
        user_profile = UserProfile.objects.get(rfid_tag=rfid_r)
        exercise_unit_r = validated_data['exercise_unit']
        active = validated_data.pop('active')

        # Create a new TrainUnit and ExerciseUnit if necessary.
        if exercise_unit_r == "None" or exercise_unit_r == "":
            # If there already exists a TrainUnit, update the end_time_date-field.
            if TrainUnit.objects.filter(date=timezone.now(), user=user_profile).exists():
                train_unit = TrainUnit.objects.get(date=timezone.now(), user=user_profile)
                train_unit.end_time_date = timezone.now()
            else:
                train_unit = TrainUnit.objects.create(date=timezone.now(), start_time_date=timezone.now(),
                                                      end_time_date=timezone.now(), user=user_profile)
            if train_unit.exercise_units.filter(exercise=Exercise.objects.get(name=exercise_name_r)).exists():
                exercise_unit_r = train_unit.exercise_units.get(exercise=Exercise.objects.get(name=exercise_name_r))
            else:
                exercise_unit_r = ExerciseUnit.objects.create(time_date=timezone.now(),
                                                        train_unit=train_unit,
                                                        exercise=Exercise.objects.get(name=exercise_name_r))
            validated_data['exercise_unit'] = exercise_unit_r
            train_unit.exercise_units.add(exercise_unit_r)
            train_unit.save()

        # Set has to be added to existing exercise unit:
        else:
            validated_data['exercise_unit'] = ExerciseUnit.objects.filter(id=validated_data['exercise_unit'])[0]
        validated_data['durations'] = json.dumps(validated_data['durations'])
        new_set = Set.objects.create(**validated_data)

        if active == 'True':
            user_profile.active_set = new_set
            user_profile.save()

        return new_set

    def update(self, instance, validated_data):
        """
        Only allows to increase the repetitions count (extra functionality for equipment components).
        """
        instance.repetitions = max(int(validated_data.get('repetitions')), int(instance.repetitions))
        instance.weight = validated_data.get('weight')
        # TODO: Logikpruefung fuer Gewicht: Siginifikant kleiner/groesser sodass waehrend Set verstellt?

        # Check whether set is still active.
        if validated_data.get('active') != 'True':
            user_profile = UserProfile.objects.get(rfid_tag=validated_data.get('rfid'))
            user_profile.active_set = None
            user_profile.save()
        instance.save()
        return instance

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
        if value < 0:
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


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(required=False, read_only=True, allow_null=True)

    class Meta:
        model = UserProfile
        fields = (['user', 'rfid_tag', 'active_set'])

