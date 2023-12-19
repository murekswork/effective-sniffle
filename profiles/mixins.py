from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages




class ProfileRequiredMixin:

    profile_create_url = 'profile_create'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not hasattr(request.user, 'profile'):
            messages.success(request, 'FIll profile before')
            print('Message shud be here')
            return redirect(self.profile_create_url)
        print('2142512215')
        return super().dispatch(request, *args, **kwargs)
