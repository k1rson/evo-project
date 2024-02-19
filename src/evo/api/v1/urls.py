from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('auth-api/', include('api.v1.api_auth_app.urls')),
    path('chat-room-api/', include('api.v1.api_chat_app.urls'))
]