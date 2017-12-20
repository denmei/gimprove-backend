from django.conf.urls import url, include
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^signup', views.sign_up, name='signup'),
]