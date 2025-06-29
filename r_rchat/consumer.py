from channels.generic.websocket import WebsocketConsumer
from .models import ChatGroup,GroupMessages
from django.template.loader import render_to_string
import json
from django.shortcuts import get_object_or_404
from asgiref.sync import async_to_sync

class ChatRoomConsumer(WebsocketConsumer):
    def connect(self):
        self.user=self.scope['user']    
        self.chatroom_name=self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom=get_object_or_404(ChatGroup,group_name=self.chatroom_name)
        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name,self.channel_name
        )
        if self.user not in self.chatroom.user_online.all():
            self.chatroom.user_online.add(self.user)
            self.update_online_count()
        self.accept()
    
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json['body']
        
        message = GroupMessages.objects.create(
            body = body,
            author = self.user, 
            group = self.chatroom 
        )
        event = {
            'type': 'message_handler',
            'message_id': message.id,
        }
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event
        )

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name,self.channel_name
        )
        if self.user in self.chatroom.user_online.all():
            self.chatroom.user_online.remove(self.user)
            self.update_online_count() 

    def message_handler(self, event):
        try:
            message_id = event['message_id']
            message = GroupMessages.objects.get(id=message_id)
            context = {
                'message': message,
                'user': self.user,
                'chat_group': self.chatroom
            }
            html = render_to_string("r_chat/partials/chat_messages_p.html", context=context)
            self.send(text_data=html)
        except Exception as e:
            print("Error in message_handler:", e)

    def update_online_count(self):
        online_count = self.chatroom.user_online.count() -1
        event = {
            'type': 'online_count_handler',
            'online_count': online_count
        }
        async_to_sync(self.channel_layer.group_send)(self.chatroom_name, event)

    def online_count_handler(self, event):
        online_count = event['online_count']      
        context = {
            'online_count' : online_count,
        }
        html = render_to_string("r_chat/partials/online_count.html", context)
        self.send(text_data=html) 