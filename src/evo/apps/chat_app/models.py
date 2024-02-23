from django.db import models

from ..authentication_app.models import CustomUser

class ChatRoomModel(models.Model):
    room_name = models.CharField(verbose_name='Название общего чата', max_length=355, unique=True)
    room_owner = models.ForeignKey(CustomUser, verbose_name='Создатель чата', on_delete=models.CASCADE, db_index=True)
    room_avatar = models.ImageField('Аватар комнаты', upload_to='chat_rooms/avatars/%Y-%m')

    def __str__(self) -> str:
        return f'{self.room_name}'
    
    class Meta:
        verbose_name = 'Общий чат'
        verbose_name_plural = 'Общие чаты'

class UserChatRoomModel(models.Model):
    user_id = models.ForeignKey(CustomUser, verbose_name='Пользователь', on_delete=models.CASCADE, db_index=True)
    room_id = models.ForeignKey(ChatRoomModel, verbose_name='Чат', on_delete=models.CASCADE, db_index=True)

    class Meta:
        verbose_name = 'Связь общих чатов и пользователей'
        verbose_name_plural = 'Связь общих чатов и пользователей'

class MessageModel(models.Model):
    sender_id = models.ForeignKey(CustomUser, verbose_name='Отправитель', related_name='sent_messages', on_delete=models.CASCADE, db_index=True)
    room_id = models.ForeignKey(ChatRoomModel, verbose_name='Чат', on_delete=models.CASCADE, db_index=True)
    text_message = models.TextField(verbose_name='Текст сообщения')
    timestamp = models.DateTimeField(verbose_name='Время отправления', auto_now_add=True)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'