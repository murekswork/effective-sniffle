from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView

from profiles.models import Profile
from .mixins import ChatAccessMixin
from .models import Chat, Message
from .forms import MessageForm


class ChatView(LoginRequiredMixin, ChatAccessMixin, DetailView):
    model = Chat
    template_name = 'chats/chat.html'

    def get_context_data(self, **kwargs):
        chat_messages = Message.objects.filter(chat=self.get_object())
        form = MessageForm
        return {'messages': chat_messages, 'form': form}

    def post(self, request, *args, **kwargs):
        sender = self.request.user.profile
        receiver = None
        chat = self.get_object()
        print(chat, 'ASTASTKO')
        if sender == self.model.profile1:
            receiver = chat.profile2
        else:
            receiver = chat.profile1
        content = self.request.POST.get('text')
        new_message = Message.objects.create(
            sender=self.request.user.profile,
            receiver=receiver,
            text=content,
            chat=chat
        )
        return redirect(reverse('chat', args=[chat.id]))





class ChatsPageView(ListView):
    model = Chat
    context_object_name = 'chats'
    template_name = 'chats/chats.html'

    def get_queryset(self):
        profile = self.request.user.profile
        return Chat.objects.filter(Q(profile1=profile) | Q(profile2=profile))

# Create your views here.
