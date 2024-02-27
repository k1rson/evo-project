from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from apps.chat_app.models import ChatRoomModel, UserChatRoomModel, ChatRoomInvitationModel
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
        return f'{obj.room_owner.last_name} {obj.room_owner.first_name}'
    
    def get_participants(self, obj):
        participants = UserChatRoomModel.objects.filter(room_id=obj).values('user_id__last_name', 'user_id__first_name')[:5]
        formatted_participants = [f"{participant['user_id__last_name']} {participant['user_id__first_name']}" for participant in participants]

        return formatted_participants

class ChatRoomActionsSerializer(serializers.ModelSerializer):
    """Сериализатор для представления создания, обновления, удаления и других различных манипуляций с общими чатами"""
    invited_users_ids = serializers.ListField(child=serializers.IntegerField(), required=False, allow_null=True)
    room_avatar = Base64ImageField()

    class Meta:
        model = ChatRoomModel
        fields = ['room_name', 'room_owner', 'room_avatar', 'invited_users_ids']

    def validate_invited_users_ids(self, value):
        users_obj = []
        for user_id in value:
            try:
                user = CustomUser.objects.get(id=user_id)
                users_obj.append(user)
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError(detail=
                    f'Пользователь с идентификатором {user_id} не существует в системе.'
                )
        return users_obj


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
        invited_users_obj = validated_data.pop('invited_users_ids', None)
        created_chat_room = ChatRoomModel.objects.create(**validated_data)

        # подписка room_owner на чат 
        relation_user_chat_room = UserChatRoomModel.objects.create(user_id=validated_data['room_owner'], room_id=created_chat_room)
        if not relation_user_chat_room: 
            raise serializers.ValidationError(detail={'relation_user_chat_room': 'Связь между пользователем-создателем и чатом не была создана. Ошибка системы, обратитесь к разработчику'})
        
        # создание приглашений в чат
        if invited_users_obj:
            for user_id in invited_users_obj:
                try:
                    ChatRoomInvitationModel.objects.create(room=created_chat_room, inviting_user=validated_data['room_owner'], invited_user=user_id)
                except Exception as e:
                    print(f'ex: {e}')

        
        return created_chat_room
    
    def update(self, instance, validated_data):
        ...

class InvitationChatRoomSerializer(serializers.ModelSerializer):
    """Сериализатор для представления чатов, в которых приглашают текущего пользователя"""
    inviting_user = serializers.SerializerMethodField()
    room_avatar = serializers.SerializerMethodField()
    room_name = serializers.SerializerMethodField()
    room_owner = serializers.SerializerMethodField()
    room_id = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoomInvitationModel
        fields = ['room_id', 'inviting_user', 'room_avatar', 'room_name', 'room_owner']

    def get_inviting_user(self, instance):
        return f'{instance.inviting_user.last_name} {instance.inviting_user.first_name}'

    def get_room_avatar(self, instance):
        return instance.room.room_avatar.url
    
    def get_room_name(self, instance):
        return instance.room.room_name

    def get_room_owner(self, instance):
        user = instance.room.room_owner
        return f'{user.last_name} {user.first_name}'
    
    def get_room_id(self, instance):
        return instance.room.id

class SearchTargetUserSerializer(serializers.ModelSerializer):
    """Сериализатор для представления поиска пользователей в системе"""
    src_avatar = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['pk', 'last_name', 'first_name', 'src_avatar']

    def get_src_avatar(self, obj):
        return obj.src_avatar.url