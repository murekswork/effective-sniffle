from django.urls import path, include
from .views import BotsLogicSendLikesView, BotsBotPageView, bot_send_like, bot_create_new, BotsProfileUpdate

urlpatterns = [
    path('bots/', BotsLogicSendLikesView.as_view(), name='bots-logic-send-likes'),
    path('bots/create_new<str:gender>~<str:orientation>/', bot_create_new, name='bots-logic-create-new'),
    path('bot/<str:pk>/', BotsBotPageView.as_view(), name='bot_page'),
    path('bot/<str:pk>/send_likes/', bot_send_like, name='bot_send_likes'),
    path('bot/<uuid:pk>/profile_update/', BotsProfileUpdate.as_view(), name='bot-profile-update'),

]