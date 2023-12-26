from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView

from profiles.mixins import ProfileRequiredMixin
from profiles.models import Profile
from .mixins import ChatAccessMixin
from .models import Chat, Message
from .forms import MessageForm


def chat(request, pk):
    chat = Chat.objects.get(id=str(pk))
    if request.user.profile not in chat.get_chat_profiles():
        return redirect('profile_chats')
    chat_messages = chat.chat_messages.select_related()
    return render(request, 'chats/chat.html', context={'chat': chat, 'chat_messages': chat_messages})






class ChatsPageView(LoginRequiredMixin, ProfileRequiredMixin, ListView):
    model = Chat
    context_object_name = 'chats'
    template_name = 'chats/chats.html'

    def get_queryset(self):
        profile = self.request.user.profile
        return profile.chat_set.select_related()

# Create your views here.
