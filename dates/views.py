from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, View

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





# Create your views here.
