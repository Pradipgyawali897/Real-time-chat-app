from django.urls import re_path
from .consumer import ChatRoomConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<chatroom_name>\w+)/$', ChatRoomConsumer.as_asgi()),
]