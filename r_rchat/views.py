# r_chat/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ChatGroup, GroupMessage, Friendship,PrivateMessage
from .forms import CreateMessage, CreateGroup
from django.http import JsonResponse
from django.db import models
import json
from .models import User
@login_required
def chat_view(request):
    chat_group = get_object_or_404(ChatGroup, group_name='public_chat')
    messages = GroupMessage.objects.filter(group=chat_group).order_by('-created')[:30]
    groups = ChatGroup.objects.filter(members=request.user)[:30]
    friendships = Friendship.objects.filter(from_user=request.user)[:12]
    group_form = CreateGroup(user=request.user)
    form = CreateMessage()

    if request.htmx:
        form = CreateMessage(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            return render(request, "r_chat/chat_message.html", {
                'message': message,
                'user': request.user,
                'chat_group': chat_group,
            })

    return render(request, "r_chat/chat.html", {
        'messages': messages,
        'form': form,
        'groups': groups,
        'friendships': friendships,
        'user': request.user,
        'public_chat': chat_group,
        'group_form': group_form,
    })

@login_required
def create_group(request):
    group_form = CreateGroup(user=request.user)
    if request.method == 'POST':
        group_form = CreateGroup(request.POST, request.FILES, user=request.user)
        if group_form.is_valid():
            chat_group = group_form.save()
            chat_group.members.add(request.user)
            friends = group_form.cleaned_data['friends']
            if friends:
                chat_group.members.add(*friends)
            return redirect('chat_view')
        else:
            groups = ChatGroup.objects.filter(members=request.user)[:30]
            friendships = Friendship.objects.filter(from_user=request.user)[:12]
            public_chat = get_object_or_404(ChatGroup, group_name='public_chat')
            return render(request, 'r_chat/partials/group_form_modal.html', {
                'group_form': group_form,
                'groups': groups,
                'friendships': friendships,
                'public_chat': public_chat,
                'user': request.user,
            })
    groups = ChatGroup.objects.filter(members=request.user)[:30]
    friendships = Friendship.objects.filter(from_user=request.user)[:12]
    return render(request, 'r_chat/partials/group_form_modal.html', {
        'group_form': group_form,
        'groups': groups,
        'friendships': friendships,
    })

@login_required
def group_detail(request, group_id):
    group = get_object_or_404(ChatGroup, id=group_id, members=request.user)
    messages = GroupMessage.objects.filter(group=group).order_by('-created')[:30]
    groups = ChatGroup.objects.filter(members=request.user)[:30]
    friendships = Friendship.objects.filter(from_user=request.user)[:12]
    form = CreateMessage()
    group_form = CreateGroup(user=request.user)
    return render(request, 'r_chat/chat.html', {
        'group': group,
        'messages': messages,
        'form': form,
        'groups': groups,
        'friendships': friendships,
        'user': request.user,
        'public_chat': group,
        'group_form': group_form,
    })

@login_required
def api_friends(request):
    friendships = Friendship.objects.filter(from_user=request.user)
    friends = [{
        'id': f.to_user.id,
        'username': f.to_user.username,
        'is_online': f.to_user in ChatGroup.objects.get(group_name='public_chat').online_users.all()
    } for f in friendships]
    return JsonResponse({'friends': friends})

@login_required
def api_friend_chat(request, friend_id):
    friend = get_object_or_404(User, id=friend_id)
    messages = PrivateMessage.objects.filter(
        models.Q(sender=request.user, receiver=friend) | 
        models.Q(sender=friend, receiver=request.user)
    ).order_by('timestamp')[:30]
    return JsonResponse({
        'friend_username': friend.username,
        'messages': [{
            'sender_id': m.sender.id,
            'content': m.content,
            'timestamp': m.timestamp.strftime('%Y-%m-%d %H:%M')
        } for m in messages]
    })

@login_required
def api_friend_chat_send(request, friend_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message')
        friend = get_object_or_404(User, id=friend_id)
        PrivateMessage.objects.create(
            sender=request.user,
            receiver=friend,
            content=message
        )
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)
def show_friends():
    pass