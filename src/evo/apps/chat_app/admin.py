from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import ChatRoomModel, MessageModel, UserChatRoomModel, ChatRoomInvitationModel

class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('room_name', 'room_owner',)
    list_filter = ('room_name', 'room_owner',)

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender_id', 'room_id', 'timestamp',)
    list_filter = ('sender_id', 'room_id', 'timestamp',)

class UserChatRoomAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'room_id',)
    list_filter = ('user_id', 'room_id',)

class ChatRoomInvitationAdmin(admin.ModelAdmin):
    list_display = ('room', 'inviting_user', 'invited_user')
    list_filter = ('room', 'inviting_user', 'invited_user')

admin.site.register(ChatRoomModel, ChatRoomAdmin)
admin.site.register(MessageModel, MessageAdmin)
admin.site.register(UserChatRoomModel, UserChatRoomAdmin)
admin.site.register(ChatRoomInvitationModel, ChatRoomInvitationAdmin)