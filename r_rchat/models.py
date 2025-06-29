from django.db import models
from django.contrib.auth.models import User


class ChatGroup(models.Model):
    group_name=models.CharField(max_length=50,unique=True)
    user_online=models.ManyToManyField(User,blank=True)
    
    def __str__(self):
        return self.group_name
    
class GroupMessages(models.Model):
    group=models.ForeignKey(ChatGroup,on_delete=models.CASCADE)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    body=models.CharField(max_length=300)
    created=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.group} \t {self.body}"
    class Meta:
        ordering = ['-created']

class Friends(models.Model):
    user_friends=models.ManyToManyField(User)
    def __str__(self):
        return f"{self.friend} \t {self.message}"
    
class Privatemessage(GroupMessages):
    friend=models.ForeignKey(Friends,on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.friend} \t {self.body}"
    

    