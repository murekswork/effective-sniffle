import json
import uuid

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async

from profiles.models import Profile
from .models import Message, Chat

from channels.generic.websocket import AsyncWebsocketConsumer
from django.core import serializers


class ChatConsumer(AsyncWebsocketConsumer):

    chat = None
    chat_id_stripped = None
    request_profile = None

    def get_request_profile(self):
        profile = Profile.objects.get(user_id=self.scope['user'].id)
        with open('logs.txt', 'w+') as f:
            f.write(f'{profile.first_name}')
        return profile.first_name

    def send_message(self, text, chat):
        self.request_profile = self.scope['user'].profile
        chat_profiles = [profile for profile in chat.get_chat_profiles()]
        if self.request_profile == chat_profiles[0]:
            message_receiver = chat_profiles[1]
        else:
            message_receiver = chat_profiles[0]
        Message.objects.create(text=text, receiver=message_receiver, sender=self.request_profile, chat=chat)

    def get_last_message(self):
        try:
            return Message.objects.last().text
        except:
            pass

    async def get_chat_messages(self):
        return database_sync_to_async(Message.objects.all)()

    async def connect(self):
        user_profile = await database_sync_to_async(Profile.objects.get)(user=self.scope['user'])
        self.chat_name = self.scope['url_route']['kwargs']['uuid']
        with open('logs.txt', 'w+') as f:
            f.write(f'{self.chat_name}123')
        self.chat = await database_sync_to_async(Chat.objects.get)(id=uuid.UUID(self.chat_name))
        print(self.chat_id_stripped)
        chat_users = await database_sync_to_async(self.chat.get_chat_profiles)()
        self.chat_group_name = f"chat_{self.chat_name}"
        if user_profile in chat_users:


            # Join chat group
            await self.channel_layer.group_add(self.chat_group_name, self.channel_name)

            await self.accept()


    async def disconnect(self, close_code):
        # Leave chat group
        await self.channel_layer.group_discard(self.chat_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        sender = await database_sync_to_async(self.get_request_profile)()

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