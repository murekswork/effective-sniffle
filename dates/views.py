from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, View, DetailView, TemplateView

from like.models import LikeModel, DislikeModel
from profiles.mixins import ProfileRequiredMixin
from profiles.models import Profile


#Util database query functions
from profiles.profiles_database_queryset_utl_functions import get_filtered_profiles

class PublicPageView(LoginRequiredMixin, ProfileRequiredMixin, ListView):
    model = Profile
    template_name = 'dates/public.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        profile_set = get_filtered_profiles(self.request.user.profile)

        return profile_set


class MeetsPageView(LoginRequiredMixin, ProfileRequiredMixin, TemplateView):

    model = Profile
    template_name = 'dates/meets.html'


    def get_queryset(self):
        profile_set = get_filtered_profiles(self.request.user.profile)
        return profile_set

    def get_context_data(self, **kwargs):
        context = {}
        meet_profile = self.get_queryset()
        if meet_profile:
            context['meet_profile'] = meet_profile[0]
        return context
# Create your views here.
