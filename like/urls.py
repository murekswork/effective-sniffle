from django.urls import path, include

from profiles.views import ProfileActivitySentLikesView, ProfileActivityReceivedLikesView
from .views import AjaxSendDislikeView, AjaxSendLikeView


urlpatterns = [
    path('like/<uuid:pk>/', AjaxSendLikeView.as_view(), name='ajax-send-like'),
    path('dislike/<uuid:pk>/', AjaxSendDislikeView.as_view(), name='ajax-send-dislike'),
    path('profile/i_liked/', ProfileActivitySentLikesView.as_view(), name='my_likes'),
    path('profile/liked_me/', ProfileActivityReceivedLikesView.as_view(), name='liked_me'),
]