from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404




class GetSessionContextMixin:

    def get_extra_context(self, *args, **kwargs):
        context = {}
        context['user_profile'] = self.request.user.profile
        return context

class ProfileRequiredMixin:

    profile_create_url = 'profile_create'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not hasattr(request.user, 'profile'):
            messages.success(request, 'Fill profile before access!')
            return redirect(self.profile_create_url)
        return super().dispatch(request, *args, **kwargs)


class AdminRequiredMixin(LoginRequiredMixin):

    def handle_no_permission(self):
        raise Http404

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()
