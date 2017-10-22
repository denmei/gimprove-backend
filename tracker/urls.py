from django.conf.urls import url
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^training_units/$', views.TrainingUnitsList.as_view(), name='training_units'),
    url(r'^training_unit/(?P<pk>[0-9A-Fa-f-]+)$', views.TrainingUnitDetail.as_view(), name='training_unit'),
    url(r'^profile/(?P<pk>\d+)$', views.ProfileView.as_view(), name='profile')
]