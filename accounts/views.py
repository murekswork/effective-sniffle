from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from allauth.account.views import SignupView
from django.urls import reverse_lazy


class CustomSignupView(SignupView):
    template_name = 'account/signup.html'
    success_url = reverse_lazy('profile_create')
# Create your views here.
