import uuid

from django.db import models
from django.urls import reverse

from like.models import Match
from profiles.models import Profile



class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.OneToOneField(Match, on_delete=models.CASCADE, blank=True)
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)
    profiles = models.ManyToManyField(Profile, blank=True)


    def get_last_message(self):
        return Message.objects.filter(chat=self).order_by('send_at').last()

    def get_chat_profiles(self):
        return list(self.profiles.select_related())

    def __str__(self):
        return f'Chat {self.profiles}'

    def get_absolute_url(self):
        return reverse('chat', args=[str(self.id)][:5])


class Message(models.Model):

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='message_sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='message_receiver')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, blank=True, related_name='chat_messages')
    send_at = models.DateTimeField(auto_now_add=True)
    read_status = models.BooleanField(default=False, blank=False, editable=True)
    text = models.TextField(blank=True, editable=True, max_length=1024)

    def __str__(self):
        return f'Message from {self.sender} to {self.receiver} {self.send_at}'

# Create your models here.
