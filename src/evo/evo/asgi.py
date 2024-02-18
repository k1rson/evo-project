import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.routing import ProtocolTypeRouter
from channels.auth import AuthMiddlewareStack

import apps.main_app.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evo.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            apps.main_app.routing.websocket_urlpatterns
        )
    )
})
