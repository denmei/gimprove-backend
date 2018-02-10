from tracker.serializers import *
from django.test import TestCase, Client
from datetime import datetime
from rest_framework.test import APITestCase, RequestsClient
import json

"""
Script to test the models of the tracker app.
"""


class SetSerializerTest(APITestCase):
    """
    Tests the functionality of the SetSerializer.
    """

    fixtures = ['fix.json']

    def setUp(self):
        self.c = RequestsClient()
        self.pre_http = "http://127.0.0.1:8000"
        pass

    def test_set_retrieval(self):
        response = self.c.get(self.pre_http + reverse('set_list')).status_code
        self.assertEqual(response, 200)

    def test_set_creation(self):
        """
        Using existing trainunit and existing exerciseunit.
        """
        # generate request data
        repetitions = 10
        weight = 60
        rfid = UserProfile.objects.first().rfid_tag
        train_unit = TrainUnit.objects.filter(user=UserProfile.objects.first())[0]
        exercise_unit = train_unit.exercise_units.first()
        exercise_name = exercise_unit.exercise
        date_time = exercise_unit.time_date
        equipment_id = Equipment.objects.first().id

        # make request and test
        data = {'exercise_unit': exercise_unit.id, 'repetitions': repetitions, 'weight': weight,
                'exercise_name': exercise_name, 'rfid': rfid, 'date_time': date_time, 'equipment_id': equipment_id,
                'active': False}
        response = self.c.post(self.pre_http + reverse('set_list'), data)
        self.assertEqual(response.status_code, 201)

    def test_set_creation_validators(self):
        pass

    def test_train_unit_creation(self):
        """
        Create new trainunit and exerciseunit.
        """
        pass

    def test_exercise_unit_creation(self):
        """
        Using existing trainunit but create new exerciseunit.
        """
        repetitions = 10
        weight = 60
        exercise_name = Exercise.objects.first()
        rfid = UserProfile.objects.first().rfid_tag
        date_time = timezone.now()
        equipment_id = Equipment.objects.first().id
        data = {'exercise_unit': "", 'repetitions': repetitions, 'weight': weight, 'exercise_name': exercise_name,
                'rfid': rfid, 'date_time': date_time, 'equipment_id': equipment_id, 'active': False}
        response = self.c.post(self.pre_http + reverse('set_list'), data)
        self.assertEqual(response.status_code, 201)

    def test_exercise_equipment_validation(self):
        """
        ExerciseName must fit to the specified equipment.
        """
        # generate request data
        repetitions = 10
        weight = 60
        rfid = UserProfile.objects.first().rfid_tag
        train_unit = TrainUnit.objects.filter(user=UserProfile.objects.first())[0]
        exercise_unit = train_unit.exercise_units.first()
        date_time = exercise_unit.time_date
        equipment_id = Equipment.objects.first().id

        # make request where exercise name and equipment do not match
        data = {'exercise_unit': exercise_unit.id, 'repetitions': repetitions, 'weight': weight,
                'exercise_name': 'some_name', 'rfid': rfid, 'date_time': date_time, 'equipment_id': equipment_id,
                'active': False}
        response = self.c.post(self.pre_http + reverse('set_list'), data)
        content = response.content

        # check whether error occured
        self.assertEqual(response.status_code, 400)
        self.assertIn("Exercise name does not fit to Equipment-ID.", str(content))

    def test_update(self):
        """
        Check whether sets are updated correctly.
        :return:
        """
        # data preparation
        train_set = Set.objects.all()[0]
        exercise_unit = train_set.exercise_unit
        exercise = exercise_unit.exercise
        equipment = exercise.equipment_machine.all()[0]
        train_unit = exercise_unit.train_unit
        user = train_unit.user
        data = {'repetitions':  int(train_set.repetitions) + 5, 'weight': 10,
                'exercise_name': exercise.name, 'equipment_id': str(equipment.id),
                'date_time': train_set.date_time.strftime("%Y-%m-%dT%H:%M:%SZ"), 'rfid': str(user.rfid_tag),
                'active': str(False)}

        # make update request
        url = self.pre_http + reverse('set_detail', kwargs={'pk': train_set.id})
        response = self.c.put(url, data)
        content = (json.loads(response.content.decode("utf-8")))

        # check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content['repetitions'], int(train_set.repetitions) + 5)
        self.assertEqual(content['weight'], 10)
        self.assertEqual(content['date_time'], train_set.date_time.strftime("%Y-%m-%dT%H:%M:%SZ"))
        self.assertEqual(content['exercise_unit'], str(exercise_unit.id))


class UserProfileSerializerTest(APITestCase):
    """
    Tests the functionality of the UserSerializer.
    """

    fixtures = ['fix.json']

    def setUp(self):
        self.c = RequestsClient()
        self.pre_http = "http://127.0.0.1:8000"
        self.rfid_tag = UserProfile.objects.all()[0].rfid_tag
        self.user = UserProfile.objects.all()[0].user
        self.active_set = UserProfile.objects.all()[0].active_set

    def test_userprofile_retrieval(self):
        response = self.c.get(self.pre_http + reverse('userprofile_detail', kwargs={'pk': self.user.id}))
        content = (json.loads(response.content.decode("utf-8")))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content['active_set'], str(self.active_set))