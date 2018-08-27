from django.urls import reverse, resolve
from django.test import TestCase


class UrlTest(TestCase):

    def setUp(self):
        pass

    def test_set_rest_urls(self):
        url_list = reverse('set_list')
        resolved_list = resolve(url_list)
        self.assertEqual(url_list, '/api_v0_tracker/set_list_rest/')
        self.assertEqual(resolved_list.view_name, "set_list")

        url_detail = reverse('set_detail', args=[1])
        resolved_detail = resolve(url_detail)
        self.assertEqual(url_detail, '/api_v0_tracker/set_detail_rest/1')
        self.assertEqual(resolved_detail.view_name, "set_detail")

        url_eu = reverse('set_exerciseunit_list', args=[1])
        resolved_eu = resolve(url_eu)
        self.assertEqual(url_eu, '/api_v0_tracker/set_exerciseunit_rest/1')
        self.assertEqual(resolved_eu.view_name, "set_exerciseunit_list")

    def test_exercise_unit_rest_urls(self):
        url_list = reverse('exerciseunit_list')
        resolved_list = resolve(url_list)
        self.assertEqual(url_list, '/api_v0_tracker/exerciseunit_list_rest/')
        self.assertEqual(resolved_list.view_name, "exerciseunit_list")

        url_detail = reverse('exerciseunit_detail', args=[1])
        resolved_detail = resolve(url_detail)
        self.assertEqual(url_detail, '/api_v0_tracker/exerciseunit_detail_rest/1')
        self.assertEqual(resolved_detail.view_name, "exerciseunit_detail")

        url_tu = reverse('exerciseunit_trainunit_list', args=[1])
        resolved_tu = resolve(url_tu)
        self.assertEqual(url_tu, '/api_v0_tracker/exerciseunit_trainunit_rest/1')
        self.assertEqual(resolved_tu.view_name, "exerciseunit_trainunit_list")

    def test_train_unit_rest_urls(self):
        url_list = reverse('trainunit_list')
        resolved_list = resolve(url_list)
        self.assertEqual(url_list, '/api_v0_tracker/trainunit_list_rest/')
        self.assertEqual(resolved_list.view_name, "trainunit_list")

        url_detail = reverse('trainunit_detail', args=[1])
        resolved_detail = resolve(url_detail)
        self.assertEqual(url_detail, '/api_v0_tracker/trainunit_detail_rest/1')
        self.assertEqual(resolved_detail.view_name, "trainunit_detail")

        url_user = reverse('trainunit_user_list', args=[1])
        resolved_user = resolve(url_user)
        self.assertEqual(url_user, '/api_v0_tracker/trainunit_user_rest/1')
        self.assertEqual(resolved_user.view_name, "trainunit_user_list")
