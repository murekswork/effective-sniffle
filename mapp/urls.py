from django.urls import path, include
from .views import get_user_location, map_view

urlpatterns = [
    path('map/public_map', map_view, name='map-main'),
    path('map/send_location', get_user_location, name='ajax-send-location'),
]