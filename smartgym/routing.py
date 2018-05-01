from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import tracker.routing
from django.urls import path
from tracker.consumers.SetConsumer import SetConsumer

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter([
            # tracker.routing.websocket_urlpatterns,
            path("/ws/tracker", SetConsumer),
        ])
    ),
})
