from rest_framework import serializers

from apps.chat_app.models import ChatRoomModel, UserChatRoomModel

class ChatRoomUserSerializer(serializers.ModelSerializer):
    participants = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoomModel
        fields = ['room_name', 'room_owner', 'room_avatar', 'participants']
    
    def get_participants(self, obj):
        participants = UserChatRoomModel.objects.filter(room_id=obj).values('user_id__last_name', 'user_id__first_name')[:5]
        formatted_participants = [f"{participant['user_id__last_name']} {participant['user_id__first_name']}" for participant in participants]

        return formatted_participants