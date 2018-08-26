"""gimprove URL Configuration

The `urlpatterns` list routes URLs to views.
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.views.generic import RedirectView
from django.conf.urls.i18n import i18n_patterns
from app_tracker.consumers.SetConsumer import SetConsumer
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views as rest_framework_views

urlpatterns = i18n_patterns(
    url(r'^landing_page/', include('app_landingpage.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls')),
)

urlpatterns += [
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^$', RedirectView.as_view(url='/landing_page/', permanent=True)),
    url(r'^admin/', admin.site.urls),
    url(r'^tracker/', include('app_tracker.urls.urls')),
    url(r'^api_v0_tracker/', include('api_v0.app_tracker.urls')),
    url(r'^api_v0_main/', include('api_v0.app_main.urls')),
    url(r'^/ws/tracker', SetConsumer),
]

urlpatterns += [
    url(r'^get_auth_token/$', rest_framework_views.obtain_auth_token, name='get_auth_token'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
