from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from chats.models import Chat
from like.models import LikeModel, Match, DislikeModel
from profiles.mixins import ProfileRequiredMixin
from profiles.models import Profile, Notification
from profiles.notifications_functions import create_match_notification
from django.http import JsonResponse


class AjaxSendDislikeView(LoginRequiredMixin, ProfileRequiredMixin, View):

    def get(self, request, pk, *args, **kwargs):
        sender_profile = self.request.user.profile
        receiver_profile = Profile.objects.get(user_id=pk)
        dislike = DislikeModel.objects.create(sender=sender_profile, receiver=receiver_profile).save()
        match = Match.objects.get_or_create(profile1=sender_profile, profile2=receiver_profile, dislike=True)

        return redirect(request.META.get('HTTP_REFERER'))


def send_like(sender, receiver):
    check_like_from_receiver = LikeModel.objects.filter(sender=receiver, receiver=sender)
    if check_like_from_receiver:
        Match.objects.create(profile1=sender_profile, profile2=receiver_profile)
    like = LikeModel.objects.create(sender=sender, receiver=receiver)


class AjaxSendLikeView(LoginRequiredMixin, ProfileRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):

        sender_profile = self.request.user.profile
        receiver_profile = Profile.objects.filter(user_id=pk).get()
        check_existing_like = LikeModel.check_like(sender=sender_profile, receiver=receiver_profile)
        if check_existing_like:
            messages.info(request, f'You are already liked {receiver_profile}')
            return redirect(receiver_profile.get_absolute_url())
        like = LikeModel.objects.create(sender=sender_profile, receiver=receiver_profile).save()
        check_match = LikeModel.check_like(sender=receiver_profile, receiver=sender_profile)
        if check_match:
            messages.info(request, f'Its a match with {receiver_profile}')
            Match.objects.create(profile1=sender_profile, profile2=receiver_profile).save()
            match = Match.objects.get(
                Q(profile1=sender_profile, profile2=receiver_profile) | Q(profile1=receiver_profile,
                                                                          profile2=sender_profile))
            new_chat = Chat.objects.create(match=match)
            new_chat.profiles.add(sender_profile, receiver_profile)
            new_chat.save()

            create_match_notification(sender_profile=sender_profile, receiver_profile=receiver_profile)
            create_match_notification(sender_profile=receiver_profile, receiver_profile=sender_profile)

            notification = {'message': 'You matched with',
                            'receiver_profile': f'{receiver_profile.first_name}',
                            'receiver_profile_pk': f'{receiver_profile.pk}',
                            'level': 'success'}
            return JsonResponse(notification)
        return JsonResponse({'message': None})

# class ProfileLikedPageView(LoginRequiredMixin, ListView):
#     model = Profile
#     template_name = 'likes/likes_page.html'
#     context_object_name = 'profiles'
#
#     def get_queryset(self):
#         queryset = LikeModel.objects.filter(sender_id=self.request.user.id).values('receiver')
#         profiles_set = [Profile.objects.get(user_id=i['receiver']) for i in queryset]
#         return profiles_set
#
# class LikedMePageView(LoginRequiredMixin, ListView):
#     model = Profile
#     template_name = 'likes/likes_page.html'
#     context_object_name = 'profiles'
#
#     def get_queryset(self):
#         queryset = LikeModel.objects.filter(receiver_id=self.request.user.id).values('sender')
#         profiles_set = [Profile.objects.get(user_id=i['sender']) for i in queryset]
#         return profiles_set
# Create your views here.
