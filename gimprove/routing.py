from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import app_tracker.routing
from app_tracker.consumers.SetConsumer import SetConsumer
from .TokenAuth import TokenAuthMiddleware
from django.conf.urls import url

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': TokenAuthMiddleware(
        URLRouter([
            url(app_tracker.routing.websocket_urlpatterns, SetConsumer),
        ])
    ),
})
