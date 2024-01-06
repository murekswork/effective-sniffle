import random
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, View, DetailView, TemplateView

from like.models import LikeModel, DislikeModel
from profiles.mixins import ProfileRequiredMixin
from profiles.models import Profile, UploadedProfilePictures
# Util database query functions
from profiles.profiles_database_queryset_utl_functions import get_filtered_profiles


class PublicPageView(LoginRequiredMixin, ProfileRequiredMixin, ListView):
    model = Profile
    template_name = 'dates/public.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        profile_set = get_filtered_profiles(self.request.user.profile)

        return profile_set


def ajax_get_profile(request):
    filtered_profiles = get_filtered_profiles(request.user.profile)
    if not filtered_profiles:
        return JsonResponse({'error': 'No profiles'})
    single_object = random.choice(filtered_profiles)
    profile_photo = single_object.profile_main_picture
    if not profile_photo:
        profile_photo = UploadedProfilePictures.objects.all()[0]

    single_object_data = {'first_name': single_object.first_name,
                          'last_name': single_object.last_name,
                          'pk': single_object.pk,
                          'photo_url': profile_photo.image.url,
                          'bio': single_object.bio,
                          'profile_url': single_object.get_absolute_url()}
    return JsonResponse(single_object_data)


class MeetsPageView(LoginRequiredMixin, ProfileRequiredMixin, TemplateView):
    model = Profile
    template_name = 'dates/meets.html'

    def get_queryset(self):
        profile_set = get_filtered_profiles(self.request.user.profile)
        return profile_set

    def get_context_data(self, **kwargs):
        context = dict()
        try:
            context['meet_profile'] = random.choice(
                get_filtered_profiles(request_profile=self.request.user.profile))  # if meet_profile:
        except:
            pass
        #     context['meet_profile'] = meet_profile[0]
        return context
# Create your views here.
