from rest_framework import serializers

from apps.chat_app.models import ChatRoomModel, UserChatRoomModel
from apps.authentication_app.models import CustomUser

from .utils import check_image

class ChatRoomSerializer(serializers.ModelSerializer):
    """Сериализатор для представления общих чатов в системе"""
    room_owner = serializers.SerializerMethodField()
    participants = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoomModel
        fields = ['id', 'room_name', 'room_owner', 'room_avatar', 'participants']
        
    def get_room_owner(self, obj):
        return f"{obj.room_owner.last_name} {obj.room_owner.first_name}"
    
    def get_participants(self, obj):
        participants = UserChatRoomModel.objects.filter(room_id=obj).values('user_id__last_name', 'user_id__first_name')[:5]
        formatted_participants = [f"{participant['user_id__last_name']} {participant['user_id__first_name']}" for participant in participants]

        return formatted_participants

class ChatRoomActionsSerializer(serializers.ModelSerializer):
    """Сериализатор для представления создания, обновления, удаления и других различных манипуляций с общими чатами"""

    class Meta:
        model = ChatRoomModel
        fields = ['room_name', 'room_owner', 'room_avatar']

    def validate(self, attrs):
        room_name = attrs.get('room_name', None)
        room_avatar = attrs.get('room_avatar', None)
        room_owner = attrs.get('room_owner', None)

        if len(room_name) < 4:
            raise serializers.ValidationError(detail={'room_name': 'Название комнаты должно содержать не менее 4 символов'})
        
        if not check_image(image=room_avatar):
            raise serializers.ValidationError(detail={'room_avatar': 'Некорректное изображение. Поддерживаемые форматы: .jpg, .webp, .png, .svg'})  
        
        if not room_owner:
            raise serializers.ValidationError(detail={'room_owner': 'Пользователь не указан как владелец комнаты. Ошибка системы, обратитесь к разработчику'})  
        
        return attrs

    def create(self, validated_data):
        created_chat_room = ChatRoomModel.objects.create(**validated_data)

        relation_user_chat_room = UserChatRoomModel.objects.create(user_id=validated_data['room_owner'], room_id=created_chat_room)
        if not relation_user_chat_room: 
            raise serializers.ValidationError(detail={'relation_user_chat_room': 'Связь между пользователем и чатом не была создана. Ошибка системы, обратитесь к разработчику'})

        return created_chat_room
    
    def update(self, instance, validated_data):
        ...

class SearchTargetUserSerializer(serializers.ModelSerializer):
    """Сериализатор для представления поиска пользователей в системе"""
    src_avatar = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['pk', 'last_name', 'first_name', 'src_avatar']

    def get_src_avatar(self, obj):
        return obj.src_avatar.url