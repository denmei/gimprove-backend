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

    class Meta:
        model = Set
        fields = ('id', 'date_time', 'durations', 'exercise_unit', 'repetitions', 'weight', 'rfid', 'equipment',
                  'exercise', 'active', 'auto_tracking')

    def create(self, validated_data):
        exercise_unit = validated_data['exercise_unit']
        exercise_name = validated_data['exercise']
        rfid = validated_data['rfid']

        # TODO: Implement logic for autotracking
        auto_tracking = True

        if exercise_unit is not None and exercise_unit != "":
            exercise_unit = ExerciseUnit.objects.get(id=exercise_unit)
            exercise = None
        else:
            exercise_unit = None
            exercise = Exercise.objects.get(name=exercise_name)
        new_set = Set.objects.create(repetitions=int(validated_data['repetitions']), exercise_unit=exercise_unit,
                                     weight=int(validated_data['weight']), durations=validated_data['durations'],
                                     auto_tracking=bool(auto_tracking),
                                     date_time=date_parser.parse(validated_data['date_time']),
                                     rfid=rfid, exercise=exercise)
        return new_set

    def validate(self, attrs):
        """
        Multiple validations of the input data coming from the client.
        """
        equipment_id_r = self.initial_data['equipment_id']
        exercise_unit = self.initial_data['exercise_unit']
        exercise_name_r = self.initial_data['exercise']
        durations = self.initial_data['durations']
        repetitions = self.initial_data['repetitions']
        rfid = self.initial_data['rfid']

        if (exercise_unit is None or exercise_unit == "") and ((exercise_name_r is None or exercise_name_r == "") or
                                                               (rfid is None or rfid == "")):
            raise ValidationError("Must provide at least exercise_unit or (exercise_name and rfid).")

        if exercise_unit is not None and exercise_unit != "":
            if not ExerciseUnit.objects.filter(id=exercise_unit).exists():
                raise ValidationError("ExerciseUnit does not exist.")

        if exercise_name_r is not None and exercise_name_r != "":
            if not Exercise.objects.filter(name=exercise_name_r).exists():
                raise ValidationError("Exercise %s does not exist!" % exercise_name_r)

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

    def update(self, instance, validated_data):
        """
        Only allows to increase the repetitions count (extra functionality for equipment components).
        """
        instance.repetitions = max(int(validated_data.get('repetitions')), int(instance.repetitions))
        instance.weight = int(validated_data.get('weight'))
        if instance.repetitions < int(validated_data.get('repetitions')):
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
