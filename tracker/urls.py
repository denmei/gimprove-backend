from django.conf.urls import url
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^activities/(?P<pk>\d+)$', views.ActivityView.as_view(), name='activities'),
    url(r'^training_units/$', views.TrainingUnitsList.as_view(), name='training_units'),
    url(r'^training_units/add/$', views.AddTrainingUnit.as_view(), name='add_train_unit'),
    url(r'^exercise_unit_list/(?P<pk>[0-9A-Fa-f-]+)$', views.ExerciseUnitList.as_view(), name='exercise_unit_list'),
    url(r'^exercise_unit_list/(?P<pk>[0-9A-Fa-f-]+)/add/$', views.AddExerciseUnit.as_view(), name='add_exercise_unit'),
    url(r'^exercise_unit_list/(?P<pk>[0-9A-Fa-f-]+)/delete/$', views.DeleteTrainingUnit.as_view(),
        name='delete_training_unit'),
    url(r'^profile/(?P<pk>\d+)$', views.ProfileView.as_view(), name='profile'),
    url(r'^achievements/(?P<pk>\d+)$', views.AchievementView.as_view(), name='achievements'),
    url(r'^gym/(?P<pk>\d+)$', views.GymView.as_view(), name='gym'),
    url(r'^followers/(?P<pk>\d+)$', views.FollowerView.as_view(), name='followers'),
    url(r'^profile/cre_connection/(?P<pk>\d+)$', views.create_connection, name='create_connection'),
    url(r'^profile/del_connection/(?P<pk>\d+)$', views.delete_connection, name='delete_connection'),
]