from django.urls import reverse
from django.shortcuts import redirect


class ProfileRequiredMixin:

    profile_create_url = 'profile_create'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not hasattr(request.user, 'profile'):
            return redirect(reverse(self.profile_create_url))
        return super().dispatch(request, *args, **kwargs)