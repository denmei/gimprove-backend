from django.test import TestCase

from app_tracker.models.models import UserTrackingProfile, Set, ExerciseUnit, TrainUnit, Exercise
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta
import dateutil.parser as date_parser


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

    def test_not_last_set_deletion(self):
        """
        Tests whether a set can be deleted from an exerciseunit that contains more than one set.
        """
        exercise_unit = ExerciseUnit.objects.first()
        # make sure that there are more than one set in the exerciseunit
        Set.objects.create(repetitions=2, weight=10, durations="[1,2]", auto_tracking=False, rfid="0006921147",
                           exercise_unit=exercise_unit, date_time=exercise_unit.time_date)
        delete_set = Set.objects.create(repetitions=3, weight=10, durations="[1,2,1]", auto_tracking=False, rfid="0006921147",
                           exercise_unit=exercise_unit, date_time=exercise_unit.time_date)
        self.assertTrue(exercise_unit.set_set.count() > 1)
        count_before = exercise_unit.set_set.count()
        delete_set.delete()
        self.assertEqual(count_before-1, exercise_unit.set_set.count())

    def test_last_set_deletion(self):
        """
        Tests whether a set can be deleted from an exerciseunit with only one set. The exerciseunit must also be
        deleted then.
        """
        # make sure that the exerciseunit only has one set and the corresponding trainunit has more than
        # one exerciseunit
        # Todo: Trainunit auto creation
        train_unit = TrainUnit.objects.create(start_time_date=date_parser.parse("2018-08-29 03:48:11.142234+00:00"),
                                             end_time_date=date_parser.parse("2018-08-29 04:48:11.142234+00:00"),
                                             date=date_parser.parse("2018-08-29"), user=UserTrackingProfile.objects.first())
        exercise_unit = ExerciseUnit.objects.create(time_date=date_parser.parse("2018-08-29 04:48:11.142234+00:00"),
                                                    exercise=Exercise.objects.all()[0], train_unit=train_unit)
        ExerciseUnit.objects.create(time_date=date_parser.parse("2018-08-29 04:38:11.142234+00:00"),
                                    exercise=Exercise.objects.all()[1], train_unit=train_unit)
        self.assertEqual(train_unit.exerciseunit_set.count(), 2)
        delete_set = Set.objects.create(repetitions=3, weight=10, durations="[1,2,1]", auto_tracking=False,
                                        rfid="0006921147", exercise_unit=exercise_unit, date_time=exercise_unit.time_date)
        delete_set.delete()
        self.assertEqual(train_unit.exerciseunit_set.count(), 1)

    def test_last_set_deletion_with_tu(self):
        """
        Tests whether a set can be deleted from an exerciseunit with only one set. The exerciseunit must also be
        deleted then. If the exerciseunit is the only eu of it's trainunit, the trainunit must be deleted too.
        """
        train_unit = TrainUnit.objects.create(start_time_date=date_parser.parse("2018-08-29 03:48:11.142234+00:00"),
                                              end_time_date=date_parser.parse("2018-08-29 04:48:11.142234+00:00"),
                                              date=date_parser.parse("2018-08-29"),
                                              user=UserTrackingProfile.objects.first())
        exercise_unit = ExerciseUnit.objects.create(time_date=date_parser.parse("2018-08-29 04:48:11.142234+00:00"),
                                                    exercise=Exercise.objects.all()[0], train_unit=train_unit)
        self.assertEqual(train_unit.exerciseunit_set.count(), 1)
        self.assertEqual(TrainUnit.objects.filter(id=train_unit.id).count(), 1)
        self.assertEqual(ExerciseUnit.objects.filter(id=exercise_unit.id).count(), 1)
        delete_set = Set.objects.create(repetitions=3, weight=10, durations="[1,2,1]", auto_tracking=False,
                                        rfid="0006921147", exercise_unit=exercise_unit,
                                        date_time=exercise_unit.time_date)

        delete_set.delete()
        self.assertEqual(TrainUnit.objects.filter(id=train_unit.id).count(), 0)
        self.assertEqual(ExerciseUnit.objects.filter(id=exercise_unit.id).count(), 0)

    def test_delete_active_set(self):
        """
        When an active set is deleted, the usertracking_profile's active value must be set to None.
        """
        exercise_unit = ExerciseUnit.objects.first()
        user_tracking_profile = exercise_unit.train_unit.user
        new_set = Set.objects.create(repetitions=3, weight=10, durations="[1,2,1]", auto_tracking=False,
                                     rfid="0006921147", exercise_unit=exercise_unit, date_time=exercise_unit.time_date,
                                     active=True)
        self.assertTrue(user_tracking_profile.active_set == new_set)
        new_set.delete()
        self.assertEqual(user_tracking_profile.active_set, None)
