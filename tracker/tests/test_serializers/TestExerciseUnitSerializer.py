import json
import random
from datetime import datetime
from django.test.utils import override_settings
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
        pass

    def test_exerciseunit_retrieval(self):
        response = self.c.get(self.pre_http + reverse('exerciseunit_list'))
        print(response.content)
        self.assertEqual(response.status_code, 200)

    def test_ExerciseUnit_creation(self):
        """
        ExerciseUnits may not be created manually.
        """
        pass

    @override_settings(DEBUG=True)
    def test_update_restrictions(self):
        """
        ExerciseUnits may not be updated manually.
        """
        pass

    def test_ExerciseUnit_delete(self):
        """
        When an ExerciseUnit is deleted, all corresponding sets must be deleted, too.
        """
        pass