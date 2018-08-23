#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from rest_framework.authtoken import views as authtoken_views
from tracker import views
from tracker.api_v0.views import set_serializer_view, \
    exerciseunit_serializer_view
from main.api_v0.views import userprofile_serializer_view
from tracker.api_v0.views import trainunit_serializer_view

urlpatterns = [
    url(r'^training_units/(?P<pk>\d+)$', views.TrainingUnitsList.as_view(), name='training_units'),
    url(r'^exercise_unit_list/(?P<pk>[0-9A-Fa-f-]+)$', views.ExerciseUnitList.as_view(), name='exercise_unit_list'),
    url(r'^exercise_unit_list/(?P<pk>[0-9A-Fa-f-]+)/add/$', views.AddExerciseUnit.as_view(), name='add_exercise_unit'),
    url(r'^exercise_unit_list/(?P<pk>[0-9A-Fa-f-]+)/delete/$', views.DeleteTrainingUnit.as_view(),
        name='delete_training_unit'),
    # url(r'^achievements/(?P<pk>\d+)$', views.AchievementView.as_view(), name='achievements'),
    # url(r'^followers/(?P<pk>\d+)$', views.FollowerView.as_view(), name='followers'),
    # url(r'^profile/cre_connection/(?P<pk>\d+)$', views.create_connection, name='create_connection'),
    # url(r'^profile/del_connection/(?P<pk>\d+)$', views.delete_connection, name='delete_connection'),
]

# Serializer Urls:
urlpatterns += [
    url(r'^v0/set_list_rest/$', set_serializer_view.SetList.as_view(), name='set_list'),
    url(r'^v0/set_detail_rest/(?P<pk>[0-9A-Fa-f-]+)$', set_serializer_view.SetDetail.as_view(), name='set_detail'),
    url(r'^v0/set_exerciseunit_rest/(?P<exercise_unit>[0-9A-Fa-f-]+)$',
        set_serializer_view.SetListByExerciseUnit.as_view(), name='set_exerciseunit_list'),

    url(r'^v0/exerciseunit_list_rest/$', exerciseunit_serializer_view.ExerciseUnitList.as_view(), name='exerciseunit_list'),
    url(r'^v0/exerciseunit_detail_rest/(?P<pk>[0-9A-Fa-f-]+)$', exerciseunit_serializer_view.ExerciseUnitDetail.as_view(),
        name='exerciseunit_detail'),
    url(r'^exerciseunit_trainunit_rest/(?P<train_unit>[\w\-]+)$',
        exerciseunit_serializer_view.ExerciseUnitListByTrainUnit.as_view(), name='exerciseunit_trainunit_list'),

    url(r'^v0/trainunit_list_rest/$', trainunit_serializer_view.TrainUnitList.as_view(),
        name='trainunit_list'),
    url(r'^v0/trainunit_detail_rest/(?P<pk>[0-9A-Fa-f-]+)$', trainunit_serializer_view.TrainUnitDetail.as_view(),
        name='trainunit_detail'),
    url(r'^v0/trainunit_user_rest/(?P<user>[\w\-]+)$',
        trainunit_serializer_view.TrainUnitListByUserId.as_view(), name='trainunit_user_list'),

    url(r'^v0/userprofile_detail_rest/$', userprofile_serializer_view.UserProfileDetail.as_view(),
        name='userprofile_detail'),
    url(r'^v0/userprofile_detail_rfid_rest/(?P<rfid_tag>[\w\-]+)$',
        userprofile_serializer_view.UserProfileDetailByRfid.as_view(), name='userprofile_rfid_detail'),
    url(r'^v0/userprofile_create_rest/$', userprofile_serializer_view.UserProfileCreator.as_view(),
        name='userprofile_create'),
]

urlpatterns += [
    url(r'^v0/rest-auth/', authtoken_views.obtain_auth_token)
]
