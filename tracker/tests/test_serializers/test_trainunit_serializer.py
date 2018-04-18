from rest_framework.test import APITestCase, RequestsClient

from tracker.serializers.TrainUnitSerializer import *


class TrainUnitSerializerTest(APITestCase):
    """
    Tests the functionality of the TrainUnitSerializer.
    """

    fixtures = ['fix.json']

    def setUp(self):
        self.c = RequestsClient()
        self.pre_http = "http://127.0.0.1:8000"

    def test_trainunit_retrieval(self):
        """
        Test whether list-interface works properly.
        """
        response = self.c.get(self.pre_http + reverse('trainunit_list'))
        self.assertEqual(response.status_code, 200)

    def test_trainunit_delete(self):
        """
        When a TrainUnit is deleted, all corresponding exerciseunits and sets must be deleted, too.
        """
        # get reference on a trainunit
        test_unit = TrainUnit.objects.first()
        test_id = test_unit.id
        # get count of all exerciseunits of the trainunit
        exerciseunit_count_before = len(ExerciseUnit.objects.filter(train_unit=test_unit))
        self.assertNotEqual(exerciseunit_count_before, 0)
        # get count of all sets of the trainunit
        set_count_before = 0
        for exercise_unit in ExerciseUnit.objects.filter(train_unit=test_unit):
            set_count_before += len(Set.objects.filter(exercise_unit=exercise_unit))
        self.assertNotEqual(set_count_before, 0)
        # delete trainunit
        response = self.c.delete(self.pre_http + reverse('trainunit_detail', kwargs={'pk': test_unit.id}))
        # check whether exerciseunit and its sets were deleted
        exerciseunit_count_after = len(ExerciseUnit.objects.filter(train_unit=test_unit))
        self.assertEqual(exerciseunit_count_after, 0)
        self.assertEqual(len(TrainUnit.objects.filter(id=test_id)), 0)
