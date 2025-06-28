from django.db import models
from django.contrib.auth.models import User


class ChatGroup(models.Model):
    group_name=models.CharField(max_length=50,unique=True)
    
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