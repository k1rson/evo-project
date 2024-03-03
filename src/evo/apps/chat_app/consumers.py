import json 

from channels.generic.websocket import AsyncWebsocketConsumer

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
        message = data['message']
        username = data['username']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message,
            'username': username
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