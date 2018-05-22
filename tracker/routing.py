from django.conf.urls import url
from .consumers.SetConsumer import SetConsumer

websocket_urlpatterns = [
    url(r'^ws/tracker', SetConsumer),
]
