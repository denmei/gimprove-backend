#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url

from tracker import views
from tracker.views.serializer_views import userprofile_serializer_view, set_serializer_view, \
    exerciseunit_serializer_view, trainunit_serializer_view

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^contact$', views.contact, name='contact'),
    url(r'^about$', views.about, name='about'),
    url(r'^activities/(?P<pk>\d+)$', views.ActivityListView.as_view(), name='activities'),
    url(r'^mockup/(?P<pk>\d+)$', views.AppMockupView.as_view(), name='mockup'),
    url(r'^training_units/(?P<pk>\d+)$', views.TrainingUnitsList.as_view(), name='training_units'),
    url(r'^exercise_unit_list/(?P<pk>[0-9A-Fa-f-]+)$', views.ExerciseUnitList.as_view(), name='exercise_unit_list'),
    url(r'^exercise_unit_list/(?P<pk>[0-9A-Fa-f-]+)/add/$', views.AddExerciseUnit.as_view(), name='add_exercise_unit'),
    url(r'^exercise_unit_list/(?P<pk>[0-9A-Fa-f-]+)/delete/$', views.DeleteTrainingUnit.as_view(),
        name='delete_training_unit'),
    url(r'^user_profile/(?P<pk>\d+)$', views.UserProfileView.as_view(), name='profile'),
    url(r'^achievements/(?P<pk>\d+)$', views.AchievementView.as_view(), name='achievements'),
    url(r'^gym/(?P<pk>\d+)$', views.GymView.as_view(), name='gym'),
    url(r'^followers/(?P<pk>\d+)$', views.FollowerView.as_view(), name='followers'),
    url(r'^profile/cre_connection/(?P<pk>\d+)$', views.create_connection, name='create_connection'),
    url(r'^profile/del_connection/(?P<pk>\d+)$', views.delete_connection, name='delete_connection'),
]

# Serializer Urls:
urlpatterns += [
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

    url(r'^userprofile_detail_rest/(?P<pk>[0-9A-Fa-f-]+)$', userprofile_serializer_view.UserProfileDetail.as_view(),
        name='userprofile_detail'),
    url(r'^userprofile_detail_rfid_rest/(?P<rfid_tag>[\w\-]+)$',
        userprofile_serializer_view.UserProfileDetailByRfid.as_view(), name='userprofile_rfid_detail'),
    url(r'^userprofile_create_rest/$', userprofile_serializer_view.UserProfileCreator.as_view(),
        name='userprofile_create'),
]

"""
# URLS for websockets
urlpatterns += [
    url(r'^ws/(?P<pk>\d+)$', views.set, name='set'),
]
"""