import json
import random
from datetime import datetime

from django.test.utils import override_settings
from rest_framework.test import APITestCase, RequestsClient

from tracker.serializers.SetSerializer import *


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
        durations = random.sample(range(1, 20), repetitions)
        # make request and test
        data = {'exercise_unit': exercise_unit.id, 'repetitions': repetitions, 'weight': weight,
                'exercise_name': exercise_name, 'rfid': rfid, 'date_time': date_time, 'equipment_id': equipment_id,
                'active': False, 'durations': json.dumps(durations)}
        response = self.c.post(self.pre_http + reverse('set_list'), data)
        self.assertEqual(response.status_code, 201)

    def test_train_unit_creation(self):
        """
        Create new trainunit and exerciseunit.
        """
        pass

    @override_settings(DEBUG=True)
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
        durations = random.sample(range(1, 20), repetitions)
        data = {'exercise_unit': "", 'repetitions': repetitions, 'weight': weight, 'exercise_name': exercise_name,
                'rfid': rfid, 'date_time': date_time, 'equipment_id': equipment_id, 'active': False, 'durations':
                    json.dumps(durations)}
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
        durations = random.sample(range(1, 20), repetitions)
        # make request where exercise name and equipment do not match
        data = {'exercise_unit': exercise_unit.id, 'repetitions': repetitions, 'weight': weight,
                'exercise_name': 'some_name', 'rfid': rfid, 'date_time': date_time, 'equipment_id': equipment_id,
                'active': False, 'durations': json.dumps(durations)}
        response = self.c.post(self.pre_http + reverse('set_list'), data)
        content = response.content

        # check whether error occured
        self.assertEqual(response.status_code, 400)
        self.assertIn("Exercise name does not fit to Equipment-ID.", str(content))

    @override_settings(DEBUG=True)
    def test_update(self):
        """
        Check whether sets are updated correctly. Last_update field must be updated automatically.
        :return:
        """
        # data preparation
        train_set = Set.objects.all()[0]
        exercise_unit = train_set.exercise_unit
        exercise = exercise_unit.exercise
        equipment = exercise.equipment_machine.all()[0]
        train_unit = exercise_unit.train_unit
        user = train_unit.user
        durations = random.sample(range(1, 20), int(train_set.repetitions) + 5)
        data = {'repetitions':  int(train_set.repetitions) + 5, 'weight': 10,
                'exercise_name': exercise.name, 'equipment_id': str(equipment.id),
                'date_time': train_set.date_time.strftime("%Y-%m-%dT%H:%M:%SZ"), 'rfid': str(user.rfid_tag),
                'active': str(False), 'durations': json.dumps(durations)}
        before_time = timezone.now()

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
        self.assertTrue(Set.objects.get(id=content['id']).last_update > before_time)

    @override_settings(DEBUG=True)
    def test_update_restrictions(self):
        """
        Tests whether only repetition-values that are greater than the current value are supported.
        Tests whether length of durations-field fits to repetitions.
        """
        # data preparation
        train_set = Set.objects.all()[0]
        exercise_unit = train_set.exercise_unit
        exercise = exercise_unit.exercise
        equipment = exercise.equipment_machine.all()[0]
        train_unit = exercise_unit.train_unit
        user = train_unit.user
        durations = random.sample(range(1, 20), int(train_set.repetitions) - 1)
        data = {'repetitions':  int(train_set.repetitions) - 1, 'weight': 10,
                'exercise_name': exercise.name, 'equipment_id': str(equipment.id),
                'date_time': train_set.date_time.strftime("%Y-%m-%dT%H:%M:%SZ"), 'rfid': str(user.rfid_tag),
                'active': str(False), 'durations': json.dumps(durations)}
        url = self.pre_http + reverse('set_detail', kwargs={'pk': train_set.id})
        # test correct update request. Repetitions value may not be changed since may not be decreased.
        response = self.c.put(url, data)
        content = (json.loads(response.content.decode("utf-8")))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content['repetitions'], int(train_set.repetitions))
        self.assertEqual(content['weight'], 10)
        self.assertEqual(content['date_time'], train_set.date_time.strftime("%Y-%m-%dT%H:%M:%SZ"))
        self.assertEqual(content['exercise_unit'], str(exercise_unit.id))

        # test update request with length of durations field other than repetitions count. Must throw error.
        data['durations'] = json.dumps(random.sample(range(1, 20), int(train_set.repetitions) + 4))
        response = self.c.put(url, data)
        self.assertEqual(response.status_code, 400)

    @override_settings(DEBUG=True)
    def test_delete_active(self):
        """
        Tests whether a created set can be deleted properly. Non-active as well as active sets are tested.
        """

        def get_new_set_id(active):
            """
            Creates new set.
            :return: id of the new set
            """
            rfid = UserProfile.objects.first().rfid_tag
            train_unit = TrainUnit.objects.filter(user=UserProfile.objects.first())[0]
            exercise_unit = train_unit.exercise_units.first()
            exercise_name = exercise_unit.exercise
            date_time = exercise_unit.time_date
            equipment_id = Equipment.objects.first().id
            durations = random.sample(range(1, 20), 10)
            data = {'exercise_unit': exercise_unit.id, 'repetitions': 10, 'weight': 60,
                    'exercise_name': exercise_name, 'rfid': rfid, 'date_time': date_time, 'equipment_id': equipment_id,
                    'active': active, 'durations': json.dumps(durations)}
            response = json.loads(self.c.post(self.pre_http + reverse('set_list'), data).content.decode("utf-8"))
            return response['id']

        # try deleting a non-active set
        id_1 = get_new_set_id(active=False)
        response_1 = self.c.delete(self.pre_http + reverse('set_detail', kwargs={'pk': id_1}))
        self.assertEqual(response_1.status_code, 204)

        # try deleting an active set
        id_2 = get_new_set_id(active=True)
        active_before = UserProfile.objects.first().active_set
        response_2 = self.c.delete(self.pre_http + reverse('set_detail', kwargs={'pk': id_2}))
        self.assertEqual(str(active_before), id_2)
        self.assertEqual(UserProfile.objects.first().active_set, None)
        self.assertEqual(response_2.status_code, 204)

    def test_delete_last(self):
        """
        A set must be properly deleted. If it was the last set in the exercise unit, the exercise unit must be
        deleted. If the exercise unit was the last one in the TrainUnit, the TrainUnit must be deleted.
        """
        # create single set with new train unit and exercise unit
        user = UserProfile.objects.first()
        train_unit = TrainUnit.objects.create(start_time_date=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                                              end_time_date=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                                              date=datetime.now().date(), user=user)
        exercise_unit = ExerciseUnit.objects.create(time_date=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                                                    train_unit=train_unit, exercise=Exercise.objects.first())
        set = Set.objects.create(date_time=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                                 exercise_unit=exercise_unit,
                                 repetitions=1, weight=10, durations=[0])

        # make sure that every object was created and is unique
        self.assertEqual(Set.objects.filter(id=set.id).count(), 1)
        self.assertEqual(ExerciseUnit.objects.filter(id=exercise_unit.id).count(), 1)
        self.assertEqual(TrainUnit.objects.filter(id=train_unit.id).count(), 1)

        # delete set
        response = self.c.delete(self.pre_http + reverse('set_detail', kwargs={'pk': set.id}))

        # set, exercise unit and train unit must be deleted
        self.assertEqual(Set.objects.filter(id=set.id).count(), 0)
        self.assertEqual(ExerciseUnit.objects.filter(id=exercise_unit.id).count(), 0)
        self.assertEqual(TrainUnit.objects.filter(id=train_unit.id).count(), 0)
        self.assertEqual(response.status_code, 204)