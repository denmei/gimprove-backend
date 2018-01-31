from rest_framework import status
from rest_framework.test import APITestCase
from tracker.models import *
from django.utils import timezone
from datetime import timedelta
import mock


class AccountTests(APITestCase):

    def test_create_set(self):
        """
        Ensure we can create a new set without existing exercise_unit and train_unit.
        """
        """user_profile = UserProfile.objects.create(date_of_birth="1991-11-20", rfid_tag="0006921147")
        exercise = Exercise.objects.create(name="Lat Pulldown Machine")
        gym_profile = GymProfile.objects.create()
        equipment = Equipment.objects.create(gym=gym_profile, exercises=exercise)
        equipment_id = equipment.id"""

        # no existing exercise_unit and train_unit
        url = reverse('set_list')
        data = {'date_time': '2017-12-22T09:23:00Z', 'exercise_unit': "", 'repetitions': 20, 'weight': 200,
                'rfid': '0006921147', 'exercise_name': "Lat Pulldown Machine", 'equipment_id': equipment_id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Set.objects.count(), 1)

        # TODO existing train_unit
        # TODO existing train_unit and exercise_unit



