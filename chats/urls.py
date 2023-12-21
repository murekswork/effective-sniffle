from django.urls import path, include
from .views import ChatView, ChatsPageView


urlpatterns = [
    path('chat/<uuid:pk>/', ChatView.as_view(), name='chat'),
    path('profile/chats/', ChatsPageView.as_view(), name='profile_chats'),
]