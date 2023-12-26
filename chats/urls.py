from django.urls import path, include
from .views import ChatsPageView, chat


urlpatterns = [
    path("chat/<str:pk>/", chat, name="chat"),
    path('profile/chats/', ChatsPageView.as_view(), name='profile_chats'),
]