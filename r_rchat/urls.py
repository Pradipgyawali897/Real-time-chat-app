# r_rchat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='home'),
    path('create_group/', views.create_group, name='create_group'),
    path('friends/', views.show_friends, name='show_friends'),
    path('group/<int:group_id>/', views.group_detail, name='group_detail'),
]