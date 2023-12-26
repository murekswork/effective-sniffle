from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, View, DetailView, TemplateView

from like.models import LikeModel
from profiles.mixins import ProfileRequiredMixin
from profiles.models import Profile


class PublicPageView(LoginRequiredMixin, ProfileRequiredMixin, ListView):
    model = Profile
    template_name = 'dates/public.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        profile = self.request.user.profile
        profile_set = Profile.objects.filter(Q(gender=profile.orientation) & Q(orientation=profile.gender))
        request_user_likes_list_profiles_id = LikeModel.objects.filter(sender=self.request.user.profile).values_list('receiver__user__id', flat=True)
        return profile_set.exclude(user__id__in=request_user_likes_list_profiles_id)


class MeetsPageView(LoginRequiredMixin, ProfileRequiredMixin, TemplateView):

    model = Profile
    template_name = 'dates/meets.html'


    def get_queryset(self):
        profile = self.request.user.profile
        profile_likes = LikeModel.objects.filter(sender=profile)
        profiles_liked = profile_likes.values_list('receiver__user__id', flat=True)
        meets_profile_set = Profile.objects.filter(gender=profile.orientation, orientation=profile.gender)
        #meets_profile_set_filtered = meets_profile_set.exclude(user__id__in=LikeModel.objects.filter(sender=profile).values('receiver__user__id'))
        meets_profile_set_filtered = meets_profile_set.exclude(user__id__in=profiles_liked)
        return meets_profile_set_filtered

    def get_context_data(self, **kwargs):
        context = {}
        meet_profile = self.get_queryset()
        if meet_profile:
            context['meet_profile'] = meet_profile[0]
        return context
# Create your views here.
