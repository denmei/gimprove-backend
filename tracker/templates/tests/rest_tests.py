from rest_framework import status
from rest_framework.test import APITestCase
from tracker.models import *
from django.utils import timezone
from datetime import timedelta
import mock
from mock import patch


class AccountTests(APITestCase):

    def test_create_set(self):
        """
        Ensure we can create a new set without existing exercise_unit and train_unit.
        """
        with patch('tracker.models.UserProfile') as UserFake, patch('tracker.models.Equipment') as EquipmentFake:
            User = UserFake
            User.rfid_tag = '0006921147'
            Equipment = EquipmentFake
            Equipment.id = "12456789"

            # no existing exercise_unit and train_unit
            url = reverse('set_list')
            data = {'date_time': '2017-12-22T09:23:00Z', 'exercise_unit': "", 'repetitions': 20, 'weight': 200,
                    'rfid': '0006921147', 'exercise_name': "Lat Pulldown", 'equipment_id': "12456789"}
            response = self.client.post(url, data, format='json')
            print(response)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Set.objects.count(), 1)

        # TODO existing train_unit
        # TODO existing train_unit and exercise_unit



