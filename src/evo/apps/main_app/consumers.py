import json

from datetime import datetime
from asgiref.sync import sync_to_async 

from channels.generic.websocket import AsyncWebsocketConsumer

@sync_to_async
def save_message(self, username, room, message):
    ...

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'common_chat'
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

    async def receive(self, text_data=None):
        from rest_framework.authtoken.models import Token

        if text_data is not None:
            data = json.loads(text_data)

            token_key = data['token']
            message = data['message']

            token_obj = await sync_to_async(Token.objects.get)(key=token_key)
            user_obj = await sync_to_async(lambda: token_obj.user)()

            current_date = datetime.now().strftime('%Y-%m-%d')
            current_time = datetime.now().strftime('%H:%M')

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'full_name': f'{user_obj.first_name} {user_obj.last_name}',
                    'avatar': user_obj.src_avatar.url,
                    'date': str(current_date), 
                    'time': str(current_time)
                }
            )

    async def chat_message(self, event):
        message = event['message']
        full_name = event['full_name']
        avatar = event['avatar']
        date = event['date']
        time = event['time']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': full_name, 
            'avatar': avatar,
            'date': date, 
            'time': time
        }))