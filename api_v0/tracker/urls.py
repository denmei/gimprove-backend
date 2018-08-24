#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from api_v0.tracker.views import set_serializer_view, trainunit_serializer_view
from api_v0.tracker.views import exerciseunit_serializer_view

# Serializer Urls:
urlpatterns = [
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
]
