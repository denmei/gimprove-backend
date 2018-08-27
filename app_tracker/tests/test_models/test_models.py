import time

from django.test import TestCase

from app_tracker.models.models import UserTrackingProfile, Set, ExerciseUnit, TrainUnit
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta
import datetime

"""
Script to test the models of the tracker app.
"""


class UserProfileTest(TestCase):
    """
    Not necessary since only testing Django-Stuff.
    """

    fixtures = ['fix.json']

    def setUp(self):
        self.up = UserTrackingProfile.objects.all()[0]

    def test_auto_deactivation(self):
        """
        Active sets must be deactivated automatically after 15 seconds of inactivity.
        """
        self.up.active_set = Set.objects.first()
        time.sleep(16)
        self.assertEqual(self.up.active_set, None)


class UserProfileActiveSetTest(TestCase):
    """
    Tests whether auto-deactivation of inactive sets works properly.
    """

    fixtures = ['fix.json']

    def setUp(self):
        self.up = UserTrackingProfile.objects.first()
        self.set = Set.objects.first()
        self.set.last_update = timezone.now()
        self.up.active_set = self.set

    def test_no_deactivation_after_update(self):
        time.sleep(5)
        self.set.last_update = timezone.now()
        time.sleep(11)
        self.assertTrue(self.up.active_set == self.set)

    def test_deactivation_no_update(self):
        self.up.active_set = self.set
        self.set.last_update = timezone.now() - timezone.timedelta(seconds=16)
        self.assertTrue(self.up.active_set is None)


class SetTest(TestCase):

    fixtures = ['fix.json']

    def setUp(self):
        pass

    def test_set_creation_all_parameters(self):
        """
        Tests whether a set is created properly if all necessary parameters are provided.
        """
        exercise_unit = ExerciseUnit.objects.first()
        new_set = Set.objects.create(repetitions=2, exercise_unit=exercise_unit, weight=10, durations="[1,2]",
                                     auto_tracking=False, date_time=exercise_unit.time_date, rfid="0006921147",
                                     exercise_name="Lat Pulldown")
        self.assertEqual(new_set.repetitions, 2)
        self.assertEqual(new_set.get_durations()[0], 1)
        self.assertEqual(new_set.weight, 10)
        self.assertEqual(new_set.exercise_unit, exercise_unit)

    def test_set_validation(self):
        """
        Tests whether the validation methods of the set-creation work properly.
        """
        exercise_unit = ExerciseUnit.objects.first()
        # check wrong durations
        with self.assertRaises(ValidationError):
            Set.objects.create(repetitions=2, exercise_unit=exercise_unit, weight=10, durations="[2]",
                               auto_tracking=False, date_time=exercise_unit.time_date, rfid="0006921147",
                               exercise_name="Lat Pulldown")
        # check invalid date
        with self.assertRaises(ValidationError):
            Set.objects.create(repetitions=2, exercise_unit=exercise_unit, weight=10, durations="[1,2]",
                               auto_tracking=False, date_time=(exercise_unit.time_date + timedelta(days=2)),
                               rfid="0006921147", exercise_name="Lat Pulldown")
        # check invalid repetitions
        with self.assertRaises(ValidationError):
            Set.objects.create(repetitions=-2, exercise_unit=exercise_unit, weight=10, durations="[1,2]",
                               auto_tracking=False, date_time=exercise_unit.time_date, rfid="0006921147",
                               exercise_name="Lat Pulldown")
        # check invalid weight
        with self.assertRaises(ValidationError):
            Set.objects.create(repetitions=2, exercise_unit=exercise_unit, weight=-10, durations="[1,2]",
                               auto_tracking=False, date_time=exercise_unit.time_date, rfid="0006921147",
                               exercise_name="Lat Pulldown")

        # check invalid date: date before exercise_unit
        with self.assertRaises(ValidationError):
            Set.objects.create(repetitions=2, exercise_unit=exercise_unit, weight=10, durations="[1,2]",
                               auto_tracking=False, date_time=exercise_unit.time_date - timedelta(days=2),
                               rfid="0006921147", exercise_name="Lat Pulldown")

        # check invalid input: no rfid and no exercise_unit
        with self.assertRaises(ValidationError):
            Set.objects.create(repetitions=2, weight=10, durations="[1,2]",
                               auto_tracking=False, date_time=exercise_unit.time_date,
                               exercise_name="Lat Pulldown")

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

        # Create new set and train_unit
        new_set = Set.objects.create(repetitions=2, weight=10, durations="[1,2]", auto_tracking=False,
                                     date_time=timezone.now() - timedelta(days=2), rfid="0006921147",
                                     exercise_name="Lat Pulldown")
        new_exercise_unit = new_set.exercise_unit
        new_train_unit = new_exercise_unit.train_unit
        self.assertEqual(new_exercise_unit.time_date, new_set.date_time)
        self.assertEqual(new_train_unit.start_time_date, new_set.date_time)

        # Create new set with existing trainunit
        start = timezone.now() - timedelta(hours=2)
        end = timezone.now()
        TrainUnit.objects.create(start_time_date=start, end_time_date=end,
                                 date=timezone.now(), user=UserTrackingProfile.objects.first())
        new_set_with_tu = Set.objects.create(repetitions=2, weight=10, durations="[1,2]", auto_tracking=False,
                                     date_time=timezone.now() - timedelta(days=2), rfid="0006921147",
                                     exercise_name="Lat Pulldown")
        new_exercise_unit_with_tu = new_set_with_tu.exercise_unit
        new_train_unit = new_exercise_unit_with_tu.train_unit
        self.assertEqual(new_exercise_unit.time_date, new_set.date_time)
        self.assertEqual(new_train_unit.start_time_date, new_set.date_time)
        self.assertEqual(new_train_unit.start_time_date, start)
        self.assertEqual(new_train_unit.end_time_date, end)

        # check invalid date: date in the future
        with self.assertRaises(ValidationError):
            Set.objects.create(repetitions=2, weight=10, durations="[1,2]", auto_tracking=False,
                                         date_time=timezone.now() + timedelta(seconds=5), rfid="0006921147",
                                         exercise_name="Lat Pulldown")
