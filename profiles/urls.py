from django.urls import path, include
from .views import (ProfileCreationView, ProfileOverviewView,
                    ProfileUpdateView, ProfileView, ProfileActivityMatchesView,
                    ProfileNotificationsView, profile_set_new_photo)

urlpatterns = [
    path('create/', ProfileCreationView.as_view(), name='profile_create'),
    path('overview/', ProfileOverviewView.as_view(), name='profile_overview'),
    path('edit/', ProfileUpdateView.as_view(), name='profile_update'),
    path('<uuid:pk>/', ProfileView.as_view(), name='profile'),
    path('notifications', ProfileNotificationsView.as_view(), name='notifications'),
    path('matches/', ProfileActivityMatchesView.as_view(), name='profile_matches'),
    path('update_profile_picture/<uuid:pk>/', profile_set_new_photo, name='profile_update_main_picture'),
]