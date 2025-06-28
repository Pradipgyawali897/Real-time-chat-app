from django.shortcuts import render,get_object_or_404,redirect
from .models import GroupMessages,ChatGroup
from .forms import CreateMessage
def chat_view(request):
    chat_group=get_object_or_404(ChatGroup,group_name='public_chat')
    messages=GroupMessages.objects.all()[:30]
    form=CreateMessage()
    if request.htmx:
        print("into the form")
        form=CreateMessage(request.POST)
        if form.is_valid():
            message=form.save(commit=False)
            message.author=request.user
            message.group=chat_group
            message.save()
            context={
                'messages':message,
                "user":request.user
            }
        return render(request,"r_chat/partials/chat_messages_p.html",context)
    return render(request,"r_chat/chat.html",context={'messages':messages,"form":form})