from django.urls import path, include
from .views import ChatView


urlpatterns = [
    path('chat/<uuid:pk/', ChatView.as_view(), name='chat')
]