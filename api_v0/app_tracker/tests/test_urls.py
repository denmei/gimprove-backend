"""
    url(r'^set_list_rest/$', set_serializer_view.SetList.as_view(), name='set_list'),
    url(r'^set_detail_rest/(?P<pk>[0-9A-Fa-f-]+)$', set_serializer_view.SetDetail.as_view(), name='set_detail'),
    url(r'^set_exerciseunit_rest/(?P<exercise_unit>[0-9A-Fa-f-]+)$',
        set_serializer_view.SetListByExerciseUnit.as_view(), name='set_exerciseunit_list'),

    url(r'^exerciseunit_list_rest/$', exerciseunit_serializer_view.ExerciseUnitList.as_view(), name='exerciseunit_list'),
    url(r'^exerciseunit_detail_rest/(?P<pk>[0-9A-Fa-f-]+)$', exerciseunit_serializer_view.ExerciseUnitDetail.as_view(),
        name='exerciseunit_detail'),
    url(r'^exerciseunit_trainunit_rest/(?P<train_unit>[\w\-]+)$',
        exerciseunit_serializer_view.ExerciseUnitListByTrainUnit.as_view(), name='exerciseunit_trainunit_list'),

    url(r'^trainunit_list_rest/$', trainunit_serializer_view.TrainUnitList.as_view(),
        name='trainunit_list'),
    url(r'^trainunit_detail_rest/(?P<pk>[0-9A-Fa-f-]+)$', trainunit_serializer_view.TrainUnitDetail.as_view(),
        name='trainunit_detail'),
    url(r'^trainunit_user_rest/(?P<user>[\w\-]+)$',
        trainunit_serializer_view.TrainUnitListByUserId.as_view(), name='trainunit_user_list'),
"""

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
