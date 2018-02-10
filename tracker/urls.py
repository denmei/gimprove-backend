#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.views.generic import RedirectView
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views


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

"""
Views for REST-API.
E.g.:
    - new set: http --json POST http://127.0.0.1:8000/tracker/set_list_rest/ date_time=2017-12-22T09:23:00 exercise_unit="2162f3f1-1671-4726-abef-586b7f15dae5"
    - delete set: http --json DELETE http://127.0.0.1:8000/tracker/set_detail_rest/fb5e2c57-9ed3-4cd3-9bae-022553ec7b9e
    - all sets: http http://127.0.0.1:8000/tracker/set_list_rest

"""
urlpatterns += [
    url(r'^set_list_rest/$', views.SetList.as_view(), name='set_list'),
    url(r'^set_detail_rest/(?P<pk>[0-9A-Fa-f-]+)$', views.SetDetail.as_view(), name='set_detail'),
    url(r'^userprofile_detail_rest/(?P<pk>[0-9A-Fa-f-]+)$', views.UserProfileDetail.as_view(), name='userprofile_detail')
]
