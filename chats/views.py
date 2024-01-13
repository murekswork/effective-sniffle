from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, F, BooleanField, Case, When
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView

from profiles.mixins import ProfileRequiredMixin
from profiles.models import Profile
from .mixins import ChatAccessMixin
from .models import Chat, Message
from .forms import MessageForm


class ChatCBVView(LoginRequiredMixin, ProfileRequiredMixin, DetailView):
    model = Chat
    template_name = 'chats/chat.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.profile not in Chat.objects.get(id=self.kwargs['pk']).get_chat_profiles():
            return redirect('profile_chats')
        return super(ChatCBVView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        chat_messages = self.object.chat_messages.prefetch_related('sender').order_by('send_at')
        chat_messages_with_read_status = chat_messages.annotate(
            read_st=Case(
                When(receiver=self.request.user.profile, then=True),
                default=False,
                output_field=BooleanField()
            )
        )
        chat_messages_with_read_status.filter(read_status=False).update(read_status=True)
        return {'chat': self.object, 'chat_messages': chat_messages_with_read_status}


def chat(request, pk):
    chat = Chat.objects.get(id=str(pk))
    if request.user.profile not in chat.get_chat_profiles():
        return redirect('profile_chats')
    chat_messages = chat.chat_messages.select_related()
    chat_messages.filter(receiver=request.user.profile).update(read_status=True)
    return render(request, 'chats/chat.html', context={'chat': chat, 'chat_messages': chat_messages})






class ChatsPageView(LoginRequiredMixin, ProfileRequiredMixin, ListView):
    model = Chat
    context_object_name = 'chats'
    template_name = 'chats/chats.html'

    def get_queryset(self):
        profile = self.request.user.profile
        return profile.chat_set.select_related()

# Create your views here.
