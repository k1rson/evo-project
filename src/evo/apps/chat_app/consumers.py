import json 

from channels.generic.websocket import AsyncWebsocketConsumer

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