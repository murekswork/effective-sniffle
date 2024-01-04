from django.urls import path, include

from profiles.views import ProfileActivitySentLikesView, ProfileActivityReceivedLikesView
from .views import SendDislikeView, AjaxSendLikeView


urlpatterns = [
    path('like/<uuid:pk>/', AjaxSendLikeView.as_view(), name='ajax-send-like'),
    path('dislike/<uuid:pk>/', SendDislikeView.as_view(), name='send_dislike'),
    path('profile/i_liked/', ProfileActivitySentLikesView.as_view(), name='my_likes'),
    path('profile/liked_me/', ProfileActivityReceivedLikesView.as_view(), name='liked_me'),
]