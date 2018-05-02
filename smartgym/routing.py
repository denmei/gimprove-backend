from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import tracker.routing
from django.urls import path
from tracker.consumers.SetConsumer import SetConsumer
from django.conf.urls import url

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter([
            url(tracker.routing.websocket_urlpatterns, SetConsumer)
        ])
    ),
})
