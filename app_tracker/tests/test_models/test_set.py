from django.test import TestCase

from app_tracker.models.models import UserTrackingProfile, Set, ExerciseUnit, TrainUnit, Exercise
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta


class SetTest(TestCase):

    fixtures = ['fix.json']

    def setUp(self):
        pass

    def test_set_creation_all_parameters(self):
        """
        Tests whether a set is created properly if all necessary parameters are provided.
        """
        exercise_unit = ExerciseUnit.objects.first()
        exercise = Exercise.objects.first()

        new_set = Set.objects.create(repetitions=2, exercise_unit=exercise_unit, weight=10, durations="[1,2]",
                                     auto_tracking=False, date_time=exercise_unit.time_date, rfid="0006921147",
                                     exercise=exercise)
        self.assertEqual(new_set.repetitions, 2)
        self.assertEqual(new_set.get_durations()[0], 1)
        self.assertEqual(new_set.weight, 10)
        self.assertEqual(new_set.exercise_unit, exercise_unit)

    def test_set_validation(self):
        """
        Tests whether the validation methods of the set-creation work properly.
        """
        exercise_unit = ExerciseUnit.objects.first()
        exercise = Exercise.objects.first()

        # check wrong durations
        with self.assertRaises(ValidationError):
            Set.objects.create(repetitions=2, exercise_unit=exercise_unit, weight=10, durations="[2]",
                               auto_tracking=False, date_time=exercise_unit.time_date, rfid="0006921147",
                               exercise=exercise)
        # check invalid date
        with self.assertRaises(ValidationError):
            Set.objects.create(repetitions=2, exercise_unit=exercise_unit, weight=10, durations="[1,2]",
                               auto_tracking=False, date_time=(exercise_unit.time_date + timedelta(days=2)),
                               rfid="0006921147", exercise=exercise)
        # check invalid repetitions
        with self.assertRaises(ValidationError):
            Set.objects.create(repetitions=-2, exercise_unit=exercise_unit, weight=10, durations="[1,2]",
                               auto_tracking=False, date_time=exercise_unit.time_date, rfid="0006921147",
                               exercise=exercise)
        # check invalid weight
        with self.assertRaises(ValidationError):
            Set.objects.create(repetitions=2, exercise_unit=exercise_unit, weight=-10, durations="[1,2]",
                               auto_tracking=False, date_time=exercise_unit.time_date, rfid="0006921147",
                               exercise=exercise)

        # check invalid date: date before exercise_unit
        with self.assertRaises(ValidationError):
            Set.objects.create(repetitions=2, exercise_unit=exercise_unit, weight=10, durations="[1,2]",
                               auto_tracking=False, date_time=exercise_unit.time_date - timedelta(days=2),
                               rfid="0006921147", exercise=exercise)

        # check invalid input: no rfid and no exercise_unit
        with self.assertRaises(ValidationError):
            Set.objects.create(repetitions=2, weight=10, durations="[1,2]",
                               auto_tracking=False, date_time=exercise_unit.time_date,
                               exercise=exercise)

        # check invalid input: no exercise and no exercise_unit
        with self.assertRaises(ValidationError):
            Set.objects.create(repetitions=2, weight=10, durations="[1,2]",
                               auto_tracking=False, date_time=exercise_unit.time_date, rfid="0006921147")

    def test_set_creation_no_eu_no_tu(self):
        """
        If no exercise_unit is provided, a new exercise_unit must be created automatically. If there is no train_unit
        for the current day, a new train_unit must be created, too.
        """
        TrainUnit.objects.all().delete()
        exercise = Exercise.objects.first()

        # Create new set and train_unit
        new_set = Set.objects.create(repetitions=2, weight=10, durations="[1,2]", auto_tracking=False,
                                     date_time=timezone.now() - timedelta(days=2), rfid="0006921147",
                                     exercise=exercise)
        new_exercise_unit = new_set.exercise_unit
        new_train_unit = new_exercise_unit.train_unit
        self.assertEqual(new_exercise_unit.time_date, new_set.date_time)
        self.assertEqual(new_train_unit.end_time_date, new_set.date_time)

    def test_set_creation_no_eu(self):
        """
        If no exercise_unit is provided, a new exercise_unit must be created automatically. If there is no train_unit
        for the current day, a new train_unit must be created, too.
        """
        TrainUnit.objects.all().delete()
        exercise = Exercise.objects.first()

        # Create new set with existing trainunit
        start = timezone.now() - timedelta(hours=2)
        end = timezone.now() - timedelta(hours=1)
        TrainUnit.objects.create(start_time_date=start, end_time_date=end,
                                 date=timezone.now(), user=UserTrackingProfile.objects.first())
        new_set_with_tu = Set.objects.create(repetitions=2, weight=10, durations="[1,2]", auto_tracking=False,
                                     date_time=start, rfid="0006921147", exercise=exercise)
        new_exercise_unit_with_tu = new_set_with_tu.exercise_unit
        new_train_unit = new_exercise_unit_with_tu.train_unit
        self.assertEqual(new_exercise_unit_with_tu.time_date, new_set_with_tu.date_time)
        self.assertEqual(new_train_unit.end_time_date, new_set_with_tu.date_time)

    def test_invalid_date(self):
        """
        Check invalid date: date in the future.
        """
        exercise = Exercise.objects.first()
        with self.assertRaises(ValidationError):
            Set.objects.create(repetitions=2, weight=10, durations="[1,2]", auto_tracking=False,
                               date_time=timezone.now() + timedelta(seconds=5), rfid="0006921147", exercise=exercise)
