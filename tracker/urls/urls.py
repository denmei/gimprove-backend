#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from tracker import views

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
