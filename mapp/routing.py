from django.urls import re_path
from . import consumers
import re


websocket_urlpatterns = [
    re_path(r'ws/map/public_map/', consumers.MapConsumer.as_asgi()),
    # re_path(r'ws/chat/(?P<uuid>[0-9a-f\-]{32,})/', consumers.ChatConsumer.as_asgi()),
]