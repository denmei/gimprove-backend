from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import tracker.routing
from tracker.consumers.SetConsumer import SetConsumer
from .TokenAuth import TokenAuthMiddleware
from django.conf.urls import url

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': TokenAuthMiddleware(
        URLRouter([
            url(tracker.routing.websocket_urlpatterns, SetConsumer),
        ])
    ),
})
