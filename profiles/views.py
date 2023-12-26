from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView, UpdateView, ListView

from like.models import Match, LikeModel
from .mixins import ProfileRequiredMixin
from .models import Profile, Interest
from .forms import ProfileCreationForm


class ProfileCreationView(LoginRequiredMixin, CreateView):
    form_class = ProfileCreationForm
    model = Profile
    template_name = 'profiles/profile_create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
# Create your views here.


class ProfileOverviewView(LoginRequiredMixin, ProfileRequiredMixin, TemplateView):
    template_name = 'profiles/profile_overview.html'

    def get_context_data(self, **kwargs):
        interests = self.request.user.profile.interests.select_related()
        return {'interests': interests}


class ProfileUpdateView(LoginRequiredMixin, ProfileRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileCreationForm
    success_url = reverse_lazy('profile_overview')
    template_name = 'profiles/profile_update.html'

    def get_object(self, queryset=None):
        return self.request.user.profile



class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profiles/profile.html'


class ProfileMatchesView(LoginRequiredMixin, ProfileRequiredMixin, ListView):
    model = Match
    context_object_name = 'matches'
    template_name = 'profiles/profile_matches.html'

    def get_queryset(self):
        user_profile = self.request.user.profile
        queryset = Match.objects.filter(Q(profile1=user_profile) | Q(profile2=user_profile))
        return queryset









