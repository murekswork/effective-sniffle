from django.urls import path, include
from .views import BotsLogicSendLikesView, BotsBotPageView, bot_send_like

urlpatterns = [
    path('bots/', BotsLogicSendLikesView.as_view(), name='bots-logic-send-likes'),
    path('bot/<str:pk>/', BotsBotPageView.as_view(), name='bot_page'),
    path('bot/<uuid:pk>/send_likes/', bot_send_like, name='bot_send_likes'),

]