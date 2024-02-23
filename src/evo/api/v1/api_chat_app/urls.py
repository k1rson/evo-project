from django.urls import path

from . import views

urlpatterns = [
    path('shared-chat-rooms', views.SharedChatRoomsAPI.as_view(), name='shared_chat_rooms'),
    path('user-chat-rooms', views.UserChatRoomsAPI.as_view(), name='user_chat_rooms'),
    path('invitation-chat-rooms', views.InvitationChatRoomsAPI.as_view(), name='invitation_chat_rooms'),
    path('chat-room-actions', views.ChatRoomActionsAPI.as_view(), name='chat_room_actions'),

    path('search-target-user/', views.SearchTargetUserAPI.as_view(), name='search_target_user'),
]