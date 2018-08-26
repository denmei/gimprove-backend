from app_tracker.models.models import UserTrackingProfile, TrainUnit, Set, ExerciseUnit
from rest_framework.test import APITestCase, RequestsClient
from django.urls import reverse
import json


class ExerciseUnitSerializerTest(APITestCase):
    """
    Tests the functionality of the SetSerializer.
    """

    fixtures = ['fix.json']

    def setUp(self):
        self.c = RequestsClient()
        self.pre_http = "http://127.0.0.1:8000"
        self.user = UserTrackingProfile.objects.all()[0].user_profile.user
        self.train_unit = TrainUnit.objects.first()
        self.header = {'Authorization': 'Token ' + str(self.user.auth_token)}

    def test_exerciseunit_retrieval(self):
        """
        Test whether list-interface works properly.
        """
        response = self.c.get(self.pre_http + reverse('exerciseunit_list'), headers=self.header)
        self.assertEqual(response.status_code, 200)

    def test_exerciseunit_retrieval_by_trainunit(self):
        """
        Tests whether exerciseunits for a specific trainunit can be retrieved.
        """
        response = self.c.get(self.pre_http + reverse('exerciseunit_trainunit_list',
                                                      kwargs={'train_unit': self.train_unit.id}),
                              headers=self.header)
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
        self.c.delete(self.pre_http + reverse('exerciseunit_detail', kwargs={'pk': test_unit.id}), headers=self.header)
        # check whether exerciseunit and its sets were deleted
        set_count_after = len(Set.objects.filter(exercise_unit=test_unit))
        self.assertEqual(set_count_after, 0)
        self.assertEqual(len(ExerciseUnit.objects.filter(id=test_id)), 0)
