import json

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async

from profiles.models import Profile
from .models import Message, Chat

from channels.generic.websocket import AsyncWebsocketConsumer
from django.core import serializers


class ChatConsumer(AsyncWebsocketConsumer):

    chat = None

    def send_message(self, text, chat):
        message_receiver = Chat.profiles.exclude(chat__profiles__in=[self.scope['user'].profile])
        Message.objects.create(text=text, receiver=message_receiver, sender=self.scope['user'], chat=chat)

    def get_last_message(self):
        try:
            return Message.objects.last().text
        except:
            pass

    async def get_chat_messages(self):
        return database_sync_to_async(Message.objects.all)()

    async def connect(self):
        user_profile = await database_sync_to_async(Profile.objects.get)(user=self.scope['user'])
        self.chat_name = self.scope["url_route"]["kwargs"]["chat_id"]
        self.chat = await database_sync_to_async(Chat.objects.get)(id=self.chat_name)
        chat_users = await database_sync_to_async(self.chat.get_chat_profiles)()
        if user_profile in chat_users:

            self.chat_group_name = f"chat_{self.chat_name}"

            # Join chat group
            await self.channel_layer.group_add(self.chat_group_name, self.channel_name)

            await self.accept()


    async def disconnect(self, close_code):
        # Leave chat group
        await self.channel_layer.group_discard(self.chat_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        sender = self.scope['user'].username

        # Send message to chat group
        await database_sync_to_async(self.send_message)(text=message, chat=self.chat)
        await self.channel_layer.group_send(self.chat_group_name, {'type': 'chat_message',
                                                                   'message': message,
                                                                   'sender': sender})

    # Receive message from chat group
    async def chat_message(self, event):
        message = event["message"]
        sender = event['sender']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, 'sender': sender}))