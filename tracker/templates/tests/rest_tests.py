from rest_framework import status
from rest_framework.test import APITestCase
from tracker.models import *


class AccountTests(APITestCase):

    def test_create_set(self):
        """
        Ensure we can create a new set.
        """
        UserProfile.objects.create(date_of_birth="1991-11-20", rfid_tag="0006921147")
        Exercise.objects.create(name="Lat Pulldown Machine")

        url = reverse('set_list')
        data = {'date_time': '2017-12-22T09:23:00Z', 'exercise_unit': "", 'repetitions': 20, 'weight': 200,
                'rfid': '0006921147', 'rfid2': '213'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Set.objects.count(), 1)
