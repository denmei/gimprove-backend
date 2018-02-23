#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from tracker.main import views
from tracker.main.views.serializer_views import userprofile_serializer_view, set_serializer_view

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^contact$', views.contact, name='contact'),
    url(r'^about$', views.about, name='about'),
    url(r'^activities/(?P<pk>\d+)$', views.ActivityListView.as_view(), name='activities'),
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
    url(r'^userprofile_detail_rest/(?P<pk>[0-9A-Fa-f-]+)$', userprofile_serializer_view.UserProfileDetail.as_view(),
        name='userprofile_detail'),
    url(r'^userprofile_detail_rfid_rest/(?P<rfid_tag>[\w\-]+)$',
        userprofile_serializer_view.UserProfileDetailByRfid.as_view(), name='userprofile_rfid_detail'),
    url(r'^userprofile_create_rest/$', userprofile_serializer_view.UserProfileCreator.as_view(),
        name='userprofile_create'),
]
