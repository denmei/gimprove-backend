#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from rest_framework.authtoken import views as authtoken_views
from api_v0.main.views import userprofile_serializer_view

# Serializer Urls:
urlpatterns = [
    url(r'^userprofile_detail_rest/$', userprofile_serializer_view.UserProfileDetail.as_view(),
        name='userprofile_detail'),
    url(r'^userprofile_detail_rfid_rest/(?P<rfid_tag>[\w\-]+)$',
        userprofile_serializer_view.UserProfileDetailByRfid.as_view(), name='userprofile_rfid_detail'),
    url(r'^userprofile_create_rest/$', userprofile_serializer_view.UserProfileCreator.as_view(),
        name='userprofile_create'),
]

urlpatterns += [
    url(r'^rest-auth/', authtoken_views.obtain_auth_token)
]
