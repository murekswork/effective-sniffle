from django.shortcuts import render
from django.views.generic import DetailView
from .models import Chat


class ChatView(DetailView):
    model = Chat
    template_name = 'chats/chat.html'


# Create your views here.
