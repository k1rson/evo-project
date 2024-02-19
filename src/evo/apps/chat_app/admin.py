from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import ChatRoomModel, MessageModel, UserChatRoomModel

class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('room_name', 'room_owner',)

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender_id', 'room_id', 'timestamp',)

class UserChatRoomAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'room_id',)

admin.site.register(ChatRoomModel, ChatRoomAdmin)
admin.site.register(MessageModel, MessageAdmin)
admin.site.register(UserChatRoomModel, UserChatRoomAdmin)
