from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('chat-rooms/', views.ChatRoomAPI.as_view(), name='chat-rooms'), 
]