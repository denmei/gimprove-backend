from rest_framework import serializers
import dateutil.parser as date_parser
from app_tracker.models.models import Set, Equipment, TrainUnit, ExerciseUnit, UserTrackingProfile, Exercise
import json
from django.utils import timezone
from django.core.exceptions import ValidationError
from app_main.models.models import UserProfile


# TODO: Add permission to restrict access only to authenticated equipment components
# TODO: Extra mark for sets that were tracked by equipment components


class SetSerializer(serializers.ModelSerializer):
    """
    Additional fields to identify the User and the used equipment. Exercise_unit must be defined twice, since
    it's an not nullable field in the model (redefine for serializer).
    """
    exercise_unit = serializers.PrimaryKeyRelatedField(required=False, read_only=True, allow_null=True)
    equipment_id = serializers.CharField(source="exercise_unit.equipment")
    rfid = serializers.CharField(source="exercise_unit.train_unit.user.user_profile.rfid_tag")

    class Meta:
        model = Set
        fields = ('id', 'date_time', 'durations', 'exercise_unit', 'repetitions', 'weight', 'rfid', 'equipment_id',
                  'exercise_name')

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
        user_tracking_profile = UserTrackingProfile.objects.get(user_profile=user_profile)
        exercise_unit_r = validated_data['exercise_unit']
        active = validated_data.pop('active')
        set_time_tz = date_parser.parse(validated_data['date_time'])

        # Create a new TrainUnit and ExerciseUnit if necessary.
        if exercise_unit_r == "None" or exercise_unit_r == "":
            # If there already exists a TrainUnit for this day, update the end_time_date-field.
            if TrainUnit.objects.filter(date=set_time_tz, user=user_tracking_profile).exists():
                train_unit = TrainUnit.objects.get(date=set_time_tz, user=user_tracking_profile)
                train_unit.end_time_date = set_time_tz
            else:
                train_unit = TrainUnit.objects.create(date=set_time_tz, start_time_date=set_time_tz,
                                                      end_time_date=set_time_tz, user=user_tracking_profile)
            #  check whether there already is a exercise unit for the specified exercise in the train unit
            if train_unit.exerciseunit_set.filter(exercise=Exercise.objects.get(name=exercise_name_r)).exists():
                exercise_unit_r = train_unit.exerciseunit_set.get(exercise=Exercise.objects.get(name=exercise_name_r))
            else:
                exercise_unit_r = ExerciseUnit.objects.create(time_date=set_time_tz,
                                                              train_unit=train_unit,
                                                              exercise=Exercise.objects.get(name=exercise_name_r))
            validated_data['exercise_unit'] = exercise_unit_r
        # Set has to be added to existing exercise unit:
        else:
            validated_data['exercise_unit'] = ExerciseUnit.objects.filter(id=validated_data['exercise_unit'])[0]
        validated_data['durations'] = ""
        # necessary to keep the timezone correct:
        validated_data['date_time'] = date_parser.parse(validated_data['date_time'])
        new_set = Set.objects.create(**validated_data)

        if active == 'True':
            user_tracking_profile.active_set = new_set
            user_tracking_profile.save()

        return new_set

    def update(self, instance, validated_data):
        """
        Only allows to increase the repetitions count (extra functionality for equipment components).
        """
        instance.repetitions = max(int(validated_data.get('repetitions')), int(instance.repetitions))
        instance.weight = validated_data.get('weight')
        instance.durations = validated_data.get('durations')
        instance.last_update = timezone.now()
        # TODO: Logikpruefung fuer Gewicht: Siginifikant kleiner/groesser sodass waehrend Set verstellt?

        # Check whether set is still active.
        if validated_data.get('active') != 'True':
            user_profile = UserProfile.objects.get(rfid_tag=validated_data.get('rfid'))
            user_tracking_profile = UserTrackingProfile.objects.get(user_profile=user_profile)
            user_tracking_profile.active_set = None
            user_tracking_profile.save()
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
