from django.conf.urls import url
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^training_units/$', views.TrainingUnitsList.as_view(), name='training_units'),
    url(r'^exercise_unit_list/(?P<pk>[0-9A-Fa-f-]+)$', views.ExerciseUnitList.as_view(), name='exercise_unit_list'),
    url(r'^exercise_unit_list/(?P<pk>[0-9A-Fa-f-]+)/add/$', views.add_exercise_unit, name='add_exercise_unit'),
    url(r'^profile/(?P<pk>\d+)$', views.ProfileView.as_view(), name='profile')
]