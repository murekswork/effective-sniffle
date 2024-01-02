from django.shortcuts import render
from django.views.generic import View, DetailView, UpdateView
from profiles.models import Profile
from .models import Bot
from django.db.models import Q
from like.models import Match

from django.shortcuts import redirect

from like.views import send_like
from profiles.profiles_database_queryset_utl_functions import get_filtered_profiles
from profiles.mixins import AdminRequiredMixin

class BotsProfileUpdate(AdminRequiredMixin, UpdateView):
    model = Profile
    fields = '__all__'
    context_object_name = 'profile'
    template_name = 'bots_logic/bot_profile_update.html'

def bot_send_like_db(pk):
    bot = Bot.objects.get(pk=pk)
    sender = bot.profile
    not_liked_profiles = get_filtered_profiles(request_profile=sender)
    for profile in not_liked_profiles:
        send_like(sender, profile)

def bot_send_like(request, pk, **kwargs):
    bot_send_like_db(pk=pk)
    return redirect(request.META.get('HTTP_REFERER'))

def bot_create_new(request, *args, **kwargs):
    new_bot = Bot()
    bot_user = new_bot.create_bot_user()
    bot_profile = new_bot.create_bot_profile(gender=kwargs['gender'], orientation=kwargs['orientation'])
    new_bot.save()
    return redirect(request.META.get('HTTP_REFERER'))



class BotsLogicSendLikesView(AdminRequiredMixin, View):

    template_name = 'bots_logic/send_likes.html'

    def get_context_data(self, **kwargs):
        bots = Bot.objects.all()
        profiles = Profile.objects.all()
        return {'bots': bots, 'profiles': profiles,}

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        ids = request.POST.getlist('bots_selector')
        if request.POST['option'] == 'delete':
            for id in ids:
                Bot.objects.get(pk=id).delete()
        elif request.POST['option'] == 'update-profile-photo':
            for id in ids:
                Bot.objects.get(pk=id).update_profile_photo()
        elif request.POST['option'] == 'send-likes':
            for id in ids:
                bot_send_like_db(pk=id)
        return redirect(request.META.get('HTTP_REFERER'))


class BotsBotPageView(AdminRequiredMixin, DetailView):
    model = Bot
    context_object_name = 'bot'
    template_name = 'bots_logic/bot_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filtered_profiles'] = get_filtered_profiles(self.object.profile)
        context['bot_matches'] = Match.objects.filter(Q(profile1=self.object.profile) | Q(profile2=self.object.profile))
        return context


# Create your views here.
