#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from tracker import views


urlpatters = [
    url(r'^gym/(?P<pk>\d+)$', views.GymView.as_view(), name='gym'),
    url(r'^user_profile/(?P<pk>\d+)$', views.UserProfileView.as_view(), name='profile'),
]