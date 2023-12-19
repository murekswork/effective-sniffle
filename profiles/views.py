from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView, UpdateView

from .mixins import ProfileRequiredMixin
from .models import Profile
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


class ProfileOverviewView(LoginRequiredMixin, TemplateView):
    template_name = 'profiles/profile_overview.html'


class ProfileUpdateView(LoginRequiredMixin, ProfileRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileCreationForm
    success_url = reverse_lazy('profile_overview')
    template_name = 'profiles/profile_update.html'

    def get_object(self, queryset=None):
        return self.request.user.profile