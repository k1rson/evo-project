import json
import humanize, humanize.i18n

from django.utils import timezone as tz

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from apps.authentication_app.models import CustomUser

@database_sync_to_async
def get_user(user_id):
    return CustomUser.objects.get(pk=user_id)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        user_id = data['user_id']
        text_message = data['text_message']

        user = await get_user(user_id)

        _t = humanize.i18n.activate("ru_RU")
        current_datetime = tz.now()
        formatted_datetime = humanize.naturaldate(current_datetime) + " | " + current_datetime.strftime('%H:%M')

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'user_id': user_id,
                'full_name': f'{user.last_name} {user.first_name}',
                'avatar_src': user.src_avatar.url,
                'timestamp': formatted_datetime,
                'text_message': text_message,
            }
        )
    
    # Receive message from room group
    async def chat_message(self, event):
        user_id = event['user_id']
        text_message = event['text_message']
        full_name = event['full_name']
        avatar_src = event['avatar_src']
        timestamp = event['timestamp']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'user_id': user_id,
            'full_name': full_name,
            'avatar_src': avatar_src,
            'timestamp': timestamp,
            'text_message': text_message,
        }))


class UpdateStatusUserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'update_status_group',
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            'update_status_group',
            self.channel_name
        )

    async def set_online_status_user(self, event):
        active_user_id = event['active_user_id']

        message = {
            'type': 'set_online_status_user', 
            'active_user_id': active_user_id
        }

        await self.send(text_data=json.dumps(message))

    async def set_offline_status_user(self, event):
        inactive_users_ids = event['inactive_users_ids']

        message = {
            'type': 'set_offline_status_user', 
            'inactive_users_ids': inactive_users_ids
        }

        await self.send(text_data=json.dumps(message))