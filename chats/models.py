import uuid

from django.db import models
from django.urls import reverse

from like.models import Match
from profiles.models import Profile


class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.OneToOneField(Match, on_delete=models.CASCADE, blank=True)
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='chat_profile1')
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='chat_profile2')

    def __str__(self):
        return f'Chat {self.profile1} with {self.profile2}'

    def get_absolute_url(self):
        return reverse('chat', args=[str(self.id)])


class Message(models.Model):

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='message_sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='message_receiver')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, blank=True)
    send_at = models.DateTimeField(auto_now_add=True)
    read_status = models.BooleanField(default=False, blank=False, editable=True)
    text = models.TextField(blank=True, editable=True, max_length=1024)

    def __str__(self):
        return self.id
# Create your models here.
