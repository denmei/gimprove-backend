from rest_framework.test import APITestCase, RequestsClient
from app_tracker.models.models import UserTrackingProfile, TrainUnit, ExerciseUnit, Set
from django.urls import reverse
import json


class TrainUnitSerializerTest(APITestCase):
    """
    Tests the functionality of the TrainUnitSerializer.
    """

    fixtures = ['fix.json']

    def setUp(self):
        self.c = RequestsClient()
        self.pre_http = "http://127.0.0.1:8000"
        self.rfid_tag = UserTrackingProfile.objects.all()[0].user_profile.rfid_tag
        self.user = UserTrackingProfile.objects.all()[0].user_profile.user
        self.active_set = UserTrackingProfile.objects.all()[0].active_set
        self.header = {'Authorization': 'Token ' + str(self.user.auth_token)}

    def test_trainunit_retrieval(self):
        """
        Test whether list-interface works properly.
        """
        response = self.c.get(self.pre_http + reverse('trainunit_list'), headers=self.header)
        self.assertEqual(response.status_code, 200)

    def test_trainunit_retrieval_by_user(self):
        """
        Tests whether TrainUnits for a specific user can be retrieved.
        """
        response = self.c.get(self.pre_http + reverse('trainunit_user_list', kwargs={'user': self.user.id}),
                              headers=self.header)
        content = (json.loads(response.content.decode("utf-8")))
        self.assertEqual(response.status_code, 200)

    def test_trainunit_delete(self):
        """
        When a TrainUnit is deleted, all corresponding exerciseunits and sets must be deleted, too.
        """
        # get reference on a trainunit
        test_unit = TrainUnit.objects.all()[1]
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
        response = self.c.delete(self.pre_http + reverse('trainunit_detail', kwargs={'pk': test_unit.id}), headers=self.header)
        # check whether exerciseunit and its sets were deleted
        exerciseunit_count_after = len(ExerciseUnit.objects.filter(train_unit=test_unit))
        self.assertEqual(exerciseunit_count_after, 0)
        self.assertEqual(len(TrainUnit.objects.filter(id=test_id)), 0)
