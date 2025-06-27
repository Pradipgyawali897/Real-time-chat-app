from django.shortcuts import render

def chat_view(request):
    return render(request,"r_chat/chat.html")