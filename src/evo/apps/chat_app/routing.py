from django.urls import re_path, path

from .consumers import UpdateStatusUserConsumer, ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/update-status/$', UpdateStatusUserConsumer.as_asgi()),
    path('ws/chat_room/<int:room_id>/', ChatConsumer.as_asgi()),
]