from django.shortcuts import redirect


class ChatAccessMixin:

    def dispatch(self, request, *args, **kwargs):
        chat = self.get_object()
        if request.user.profile not in [chat.profile1, chat.profile2]:
            return redirect('profile_chats')
        return super().dispatch(request, *args, **kwargs)
