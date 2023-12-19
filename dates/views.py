from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView

from profiles.mixins import ProfileRequiredMixin
from profiles.models import Profile


class PublicPageView(LoginRequiredMixin, ProfileRequiredMixin, ListView):
    model = Profile
    template_name = 'dates/public.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        return Profile.objects.filter(gender=self.request.user.profile.orientation)

# Create your views here.
