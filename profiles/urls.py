from django.urls import path, include
from .views import ProfileCreationView, ProfileOverviewView, ProfileUpdateView

urlpatterns = [
    path('create/', ProfileCreationView.as_view(), name='profile_create'),
    path('overview/', ProfileOverviewView.as_view(), name='profile_overview'),
    path('edit/', ProfileUpdateView.as_view(), name='profile_update'),
]