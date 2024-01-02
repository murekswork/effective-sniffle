from django.shortcuts import render
from django.views.generic import View, DetailView
from profiles.models import Profile
from .models import Bot
from django.db.models import Q
from like.models import Match

from django.shortcuts import redirect

from like.views import send_like
from profiles.profiles_database_queryset_utl_functions import get_filtered_profiles


def bot_send_like(request, pk, **kwargs):
    sender = Profile.objects.get(pk=pk)
    not_liked_profiles = get_filtered_profiles(request_profile=sender)
    for profile in not_liked_profiles:
        send_like(sender, profile)
    return redirect(request.META.get('HTTP_REFERER'))






class BotsLogicSendLikesView(View):

    template_name = 'bots_logic/send_likes.html'

    def get_context_data(self, **kwargs):
        bots = Bot.objects.all()
        profiles = Profile.objects.all()
        return {'bots': bots, 'profiles': profiles,}

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)


class BotsBotPageView(DetailView):
    model = Bot
    context_object_name = 'bot'
    template_name = 'bots_logic/bot_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filtered_profiles'] = get_filtered_profiles(self.object.profile)
        context['bot_matches'] = Match.objects.filter(Q(profile1=self.object.profile) | Q(profile2=self.object.profile))
        return context


# Create your views here.
