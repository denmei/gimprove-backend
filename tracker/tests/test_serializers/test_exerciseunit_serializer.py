from rest_framework.test import APITestCase, RequestsClient

from tracker.serializers.ExerciseUnitSerializer import *


class ExerciseUnitSerializerTest(APITestCase):
    """
    Tests the functionality of the SetSerializer.
    """

    fixtures = ['fix.json']

    def setUp(self):
        self.c = RequestsClient()
        self.pre_http = "http://127.0.0.1:8000"
        self.user = UserProfile.objects.all()[0].user
        self.train_unit = TrainUnit.objects.first()

    def test_exerciseunit_retrieval(self):
        """
        Test whether list-interface works properly.
        """
        response = self.c.get(self.pre_http + reverse('exerciseunit_list'))
        self.assertEqual(response.status_code, 200)

    def test_exerciseunit_retrieval_by_trainunit(self):
        """
        Tests whether exerciseunits for a specific trainunit can be retrieved.
        """
        response = self.c.get(self.pre_http + reverse('exerciseunit_trainunit_list', kwargs={'train_unit': self.train_unit}))
        content = (json.loads(response.content.decode("utf-8")))
        self.assertEqual(response.status_code, 200)

    def test_exerciseunit_delete(self):
        """
        When an ExerciseUnit is deleted, all corresponding sets must be deleted, too.
        """
        # get reference on a exerciseunit
        test_unit = ExerciseUnit.objects.first()
        test_id = test_unit.id
        # get reference on all sets of the exerciseunit
        set_count_before = len(Set.objects.filter(exercise_unit=test_unit))
        self.assertNotEqual(set_count_before, 0)
        # delete exercise unit
        self.c.delete(self.pre_http + reverse('exerciseunit_detail', kwargs={'pk': test_unit.id}))
        # check whether exerciseunit and its sets were deleted
        set_count_after = len(Set.objects.filter(exercise_unit=test_unit))
        self.assertEqual(set_count_after, 0)
        self.assertEqual(len(ExerciseUnit.objects.filter(id=test_id)), 0)
