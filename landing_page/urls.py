from django.conf.urls import url, include
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    url(r'^$', views.home, name='landing'),
    url(r'^$', views.index, name='index'),
    url(r'^contact$', views.contact, name='contact'),
    url(r'^about$', views.about, name='about'),
    # url(r'^activities/(?P<pk>\d+)$', views.ActivityListView.as_view(), name='activities'),
    url(r'^mockup/(?P<pk>\d+)$', views.AppMockupView.as_view(), name='mockup'),
]