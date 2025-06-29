import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import ChatGroup, GroupMessage

class ChatRoomConsumer(WebsocketConsumer):

    def connect(self):
        self.user = self.scope['user']
        self.group_name = self.scope['url_route']['kwargs']['chatroom_name']
        print(f"Connecting user {self.user} to group {self.group_name}")

        try:
            self.chat_group = get_object_or_404(ChatGroup, group_name=self.group_name)
        except Exception as e:
            print(f"Error fetching ChatGroup {self.group_name}: {e}")
            self.close()
            return

        if not self.user.is_authenticated:
            print(f"User not authenticated: {self.user}")
            self.close()
            return

        with transaction.atomic():
            async_to_sync(self.channel_layer.group_add)(
                self.group_name,
                self.channel_name
            )
            if not self.chat_group.online_users.filter(id=self.user.id).exists():
                self.chat_group.online_users.add(self.user)
                print(f"Added {self.user} to online_users: {list(self.chat_group.online_users.all())}")
                self.send_online_count()
                self.send_online_users()

        self.accept()
        print(f"WebSocket accepted for {self.user} in {self.group_name}")

    def disconnect(self, close_code):
        print(f"Disconnecting user {self.user} from {self.group_name}, code: {close_code}")
        with transaction.atomic():
            async_to_sync(self.channel_layer.group_discard)(
                self.group_name,
                self.channel_name
            )
            if self.chat_group.online_users.filter(id=self.user.id).exists():
                self.chat_group.online_users.remove(self.user)
                print(f"Removed {self.user} from online_users: {list(self.chat_group.online_users.all())}")
                self.send_online_count()
                self.send_online_users()

    def receive(self, text_data):
        try:
            data = json.loads(text_data)
            body = data.get('body')
            if not body:
                print("No body in message")
                return

            message = GroupMessage.objects.create(
                body=body,
                author=self.user,
                group=self.chat_group
            )
            print(f"Created message: {message}")

            html = render_to_string("r_chat/chat_message.html", {
                'message': message,
                'user': self.user,
                'chat_group': self.chat_group,
            })
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type': 'chat_message',
                    'html': html,
                }
            )
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            self.send(text_data=json.dumps({'error': 'Invalid message format'}))
        except Exception as e:
            print(f"Receive error: {e}")
            self.send(text_data=json.dumps({'error': 'Server error'}))

    def chat_message(self, event):
        try:
            self.send(text_data=event['html'])
            print(f"Sent chat message to {self.user}")
        except Exception as e:
            print(f"Chat message error: {e}")

    def send_online_users(self):
        try:
            online_users = self.chat_group.online_users.all()
            print(f"Sending online users: {list(online_users)}")
            html = render_to_string("r_chat/partials/online_users.html", {
                "users": online_users
            })
            print(f"Online users HTML: {html[:100]}...")
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type': 'online_users',
                    'html': html,
                    'hx_target': '#online-users-container',
                    'hx_swap': 'innerHTML'
                }
            )
        except Exception as e:
            print(f"Error sending online users: {e}")

    def send_online_count(self):
        try:
            count = self.chat_group.online_users.count()
            print(f"Sending online count: {count}")
            html = render_to_string("r_chat/partials/online_count.html", {
                'online_count': count
            })
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    'type': 'online_count',
                    'html': html,
                    'hx_target': '#online-count-container',
                    'hx_swap': 'innerHTML'
                }
            )
        except Exception as e:
            print(f"Error sending online count: {e}")

    def online_count(self, event):
        try:
            self.send(text_data=json.dumps({
                'html': event['html'],
                'hx_target': event['hx_target'],
                'hx_swap': event['hx_swap']
            }))
            print(f"Sent online count to {self.user}")
        except Exception as e:
            print(f"Online count error: {e}")

    def online_users(self, event):
        try:
            self.send(text_data=json.dumps({
                'html': event['html'],
                'hx_target': event['hx_target'],
                'hx_swap': event['hx_swap']
            }))
            print(f"Sent online users HTML to {self.user}")
        except Exception as e:
            print(f"Online users error: {e}")