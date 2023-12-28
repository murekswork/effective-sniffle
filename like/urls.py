from django.urls import path, include

from .views import SendDislikeView, SendLikeView, ProfileLikedPageView, LikedMePageView

urlpatterns = [
    path('like/<uuid:pk>/', SendLikeView.as_view(), name='send_like'),
    path('dislike/<uuid:pk>/', SendDislikeView.as_view(), name='send_dislike'),
    path('profile/i_liked/', ProfileLikedPageView.as_view(), name='my_likes'),
    path('profile/liked_me/', LikedMePageView.as_view(), name='liked_me'),
]