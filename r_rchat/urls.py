from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat_view'),
    path('group/<int:group_id>/', views.group_detail, name='group_detail'),
    path('create_group/', views.create_group, name='create_group'),
    path('api/friends/', views.api_friends, name='api_friends'),
    path('api/friend-chat/<int:friend_id>/', views.api_friend_chat, name='api_friend_chat'),
    path('api/friend-chat/<int:friend_id>/send/', views.api_friend_chat_send, name='api_friend_chat_send'),
]