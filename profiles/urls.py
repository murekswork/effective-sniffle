from django.urls import path, include
from .views import ProfileCreationView, ProfileOverviewView, ProfileUpdateView, ProfileView, ProfileMatchesView

urlpatterns = [
    path('create/', ProfileCreationView.as_view(), name='profile_create'),
    path('overview/', ProfileOverviewView.as_view(), name='profile_overview'),
    path('edit/', ProfileUpdateView.as_view(), name='profile_update'),
    path('<uuid:pk>/', ProfileView.as_view(), name='profile'),
    path('matches/', ProfileMatchesView.as_view(), name='profile_matches'),
]