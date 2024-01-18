import json
import uuid

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async

from mapp.models import LocationProfile
from profiles.models import Profile

from channels.generic.websocket import AsyncWebsocketConsumer
from django.core import serializers

import datetime

class MapConsumer(AsyncWebsocketConsumer):

    chat = None
    chat_id_stripped = None
    request_profile = None

    def get_request_profile(self):
        profile = Profile.objects.get(user_id=self.scope['user'].id)
        with open('logs.txt', 'w+') as f:
            f.write(f'{profile.first_name}')
        return profile


    def chat_read_messages(self):
        self.chat.chat_messages.filter(sender__user__in=[self.scope['user']]).update(read_status=True)

    def get_locations(self, sharing_locations):
        data = dict()
        for location in sharing_locations:
            profile_data = {
                'first_name': location.user.profile.first_name,
                'last_name': location.user.profile.last_name,
                'gender': location.user.profile.gender,
                'profile_url': location.user.profile.get_absolute_url(),
                'photo': location.user.profile.profile_main_picture.image.url
            }
            location_data = {
                'location_id': str(location.id),
                'latitude': str(location.latitude),
                'longitude': str(location.longitude),
                'profile': profile_data
            }
            data[str(location.id)] = location_data

        with open('test_locations.txt', 'w+') as f:
            f.write(json.dumps(data))
        return data


    async def delete_location(self, user_id):
        data = dict()
        data['location_id'] = user_id
        data['type'] = 'delete_location'
        await self.channel_layer.group_send(self.chat_group_name, text_data=json.dumps(data))



    async def connect(self):
        user_profile = await database_sync_to_async(Profile.objects.get)(user=self.scope['user'])
        sharing_locations = await database_sync_to_async(LocationProfile.objects.all)()
        locations = await database_sync_to_async(self.get_locations)(sharing_locations=sharing_locations)
        self.chat_name = 'public_map'
        self.chat_group_name = f"chat_{self.chat_name}"


        # await self.channel_layer.group_send(self.chat_group_name, locations)
        await self.channel_layer.group_add(self.chat_group_name, self.channel_name)
        await self.accept()
        await self.send(json.dumps(locations))
        # await self.send(text_data=json.dumps(sharing_locations_json))


    async def disconnect(self, close_code):
        # Leave chat group
        await self.channel_layer.group_discard(self.chat_group_name, self.channel_name)

    async def receive(self, text_data):
        message = json.loads(text_data)
        data = dict()
        data['type'] = 'chat_message'
        data['message'] = message
        with open ('test_receive.txt', 'w+') as file:
            file.write(str(data))
        await self.channel_layer.group_send(self.chat_group_name, message=data)
        await self.send(json.dumps(data))

    # Receive message from chat group
    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['message']))