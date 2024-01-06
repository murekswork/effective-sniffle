import json
import uuid

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async

from profiles.models import Profile
from .models import Message, Chat

from channels.generic.websocket import AsyncWebsocketConsumer
from django.core import serializers

import datetime

class ChatConsumer(AsyncWebsocketConsumer):

    chat = None
    chat_id_stripped = None
    request_profile = None

    def get_request_profile(self):
        profile = Profile.objects.get(user_id=self.scope['user'].id)
        with open('logs.txt', 'w+') as f:
            f.write(f'{profile.first_name}')
        return profile

    def send_message(self, sender_id, text, chat):
        sender_profile = Profile.objects.get(user_id=sender_id)
        # request_profile = self.scope['user'].profile
        chat_profiles = [profile for profile in chat.get_chat_profiles()]
        if sender_profile == chat_profiles[0]:
            message_receiver = chat_profiles[1]
        else:
            message_receiver = chat_profiles[0]
        message = Message.objects.create(text=text, receiver=message_receiver, sender=sender_profile, chat=chat)
        return message.send_at

    def get_last_message(self):
        try:
            return Message.objects.last().text
        except:
            pass

    async def get_chat_messages(self):
        return database_sync_to_async(Message.objects.all)()

    def chat_read_messages(self):
        self.chat.chat_messages.filter(sender__user__in=[self.scope['user']]).update(read_status=True)

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
            await database_sync_to_async(self.chat_read_messages)()


    async def disconnect(self, close_code):
        # Leave chat group
        await self.channel_layer.group_discard(self.chat_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        sender_id = text_data_json['sender_id']
        sender_profile_photo_url = text_data_json['sender_profile_photo_url']
        sender_name = text_data_json['sender_name']
        with open('logs1.txt', 'a') as f:
            f.write(text_data)
        sender = await database_sync_to_async(self.get_request_profile)()

        # Send message to chat group
        send_time = await database_sync_to_async(self.send_message)(text=message, chat=self.chat, sender_id=sender_id)
        await self.channel_layer.group_send(self.chat_group_name, {'type': 'chat_message',
                                                                   'message': message,
                                                                   'sender_name': sender_name,
                                                                   'sender_id': sender_id,
                                                                   'sender_profile_photo_url': sender_profile_photo_url,
                                                                   'send_time': send_time.strftime('%m-%d-%y %H:%M')})

    # Receive message from chat group
    async def chat_message(self, event):
        message = event["message"]
        sender_id = event["sender_id"]
        sender_profile_photo_url = event['sender_profile_photo_url']
        sender_name = event['sender_name']
        send_time = event['send_time']
        # send_time = str(datetime.datetime.now())
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message,
                                              'sender_id': sender_id,
                                              'sender_name': sender_name,
                                             'sender_profile_photo_url': sender_profile_photo_url,
                                              'send_time': send_time}))