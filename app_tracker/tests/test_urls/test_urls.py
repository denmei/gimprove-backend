from django.urls import reverse, resolve
from django.test import TestCase


class UrlTest(TestCase):

    def setUp(self):
        pass

    def test_training_units_urls(self):
        url = reverse('training_units', args=[1])
        resolved = resolve(url)
        self.assertEqual(url, '/tracker/training_units/1')
        self.assertEqual(resolved.view_name, "training_units")

        url_delete = reverse('delete_training_unit', args=[1])
        resolved_delete = resolve(url_delete)
        self.assertEqual(url_delete, '/tracker/training_units/1/delete/')
        self.assertEqual(resolved_delete.view_name, "delete_training_unit")

    def test_exercise_units_urls(self):
        url = reverse('exercise_unit_list', args=[1])
        resolved = resolve(url)
        self.assertEqual(url, '/tracker/exercise_unit_list/1')
        self.assertEqual(resolved.view_name, "exercise_unit_list")

        url_add = reverse('add_exercise_unit', args=[1])
        resolved_add = resolve(url_add)
        self.assertEqual(url_add, '/tracker/exercise_unit_list/1/add/')
        self.assertEqual(resolved_add.view_name, "add_exercise_unit")
