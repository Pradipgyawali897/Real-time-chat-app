
from django.urls import path
from .consumer import ChatRoomConsumer

websocket_urlpatterns = [
    path("ws/chatroom/<chatroom_name>/", ChatRoomConsumer.as_asgi()),
]
