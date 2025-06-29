from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ChatGroup, GroupMessage, Friendship
from .forms import CreateMessage, CreateGroup

@login_required
def chat_view(request):
    chat_group = get_object_or_404(ChatGroup, group_name='public_chat')
    messages = GroupMessage.objects.filter(group=chat_group).order_by('-created')[:30]
    groups = ChatGroup.objects.filter(members=request.user)[:30]
    friendships = Friendship.objects.filter(from_user=request.user)[:12]
    group_form = CreateGroup()
    form = CreateMessage()

    if request.htmx:
        form = CreateMessage(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            return render(request, "r_chat/partials/chat_messages_p.html", {
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
    form = CreateGroup()
    if request.method == 'POST':
        form = CreateGroup(request.POST, request.FILES)
        if form.is_valid():
            chat_group = form.save()
            chat_group.members.add(request.user)
            return redirect('chat_view')
        else:
            groups = ChatGroup.objects.filter(members=request.user)[:30]
            friendships = Friendship.objects.filter(from_user=request.user)[:12]
            public_chat = get_object_or_404(ChatGroup, group_name='public_chat')
            return render(request, 'r_chat/partials/group_form_modal.html', {
                'group_form': form,
                'groups': groups,
                'friendships': friendships,
                'public_chat': public_chat,
                'user': request.user,
            })
    return render(request, 'r_chat/partials/group_form_modal.html', {'form': form})

@login_required
def group_detail(request, group_id):
    group = get_object_or_404(ChatGroup, id=group_id, members=request.user)
    messages = GroupMessage.objects.filter(group=group).order_by('-created')[:30]
    groups = ChatGroup.objects.filter(members=request.user)[:30]
    friendships = Friendship.objects.filter(from_user=request.user)[:12]
    form = CreateMessage()
    return render(request, 'r_chat/chat.html', {
        'group': group,
        'messages': messages,
        'form': form,
        'groups': groups,
        'friendships': friendships,
        'user': request.user,
        'public_chat': group,  # For WebSocket group_name
        'group_form': CreateGroup(),
    })

def show_friends():
    pass