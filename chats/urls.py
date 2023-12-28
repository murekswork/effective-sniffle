from django.urls import path, include
from .views import ChatsPageView, chat, ChatCBVView


urlpatterns = [
    path("chat/<uuid:pk>/", ChatCBVView.as_view(), name="chat"),
    path('profile/chats/', ChatsPageView.as_view(), name='profile_chats'),
]