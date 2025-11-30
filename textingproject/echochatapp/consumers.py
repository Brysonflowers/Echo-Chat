import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Message, ChatGroup
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs'].get('room_name')
        self.private_chat_id = self.scope['url_route']['kwargs'].get('private_chat_id')

        if self.room_name:
            self.room_group_name = f'chat_{self.room_name}'
        elif self.private_chat_id:
            self.room_group_name = f'private_chat_{self.private_chat_id}'
        else:
            await self.close()
            return
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = self.scope["user"].username if self.scope["user"].is_authenticated else "Anonymous"

        if self.scope["user"].is_authenticated:
            if self.room_name:
                group = await sync_to_async(ChatGroup.objects.get)(name=self.room_name)
                await self.save_message(self.scope["user"], group, message)
            elif self.private_chat_id:
                # Assuming private_chat_id is something like "private_1_2" where 1 and 2 are user IDs
                # We need to extract the other user's ID
                participants = self.private_chat_id.split('_')
                other_user_id = int(participants[1]) if int(participants[0]) == self.scope["user"].id else int(participants[0])
                receiver = await sync_to_async(User.objects.get)(id=other_user_id)
                await self.save_message(self.scope["user"], None, message, receiver=receiver)

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
            'message': message,
            'username': username
        }))

    @sync_to_async
    def get_user(self, username):
        return User.objects.get(username=username)

    @sync_to_async
    def save_message(self, sender, content, group=None, receiver=None):
        Message.objects.create(sender=sender, group=group, content=content, receiver=receiver)

    #This is so the website that is asynchronous does not freeze and I added group chats and other rooms