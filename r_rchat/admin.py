from django.contrib import admin
from .models import *
admin.site.register(ChatGroup)
admin.site.register(GroupMessage)
admin.site.register(Friend)
admin.site.register(PrivateMessage)
admin.site.register(Friendship)
