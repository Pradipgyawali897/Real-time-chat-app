from django.db import models
from django.contrib.auth.models import User


class ChatGroup(models.Model):
    group_name = models.CharField(max_length=50, unique=True)
    picture = models.ImageField(upload_to="storage/group/photo", blank=True)

    # Many-to-many relations
    members = models.ManyToManyField(User, blank=True, related_name="chat_groups")
    online_users = models.ManyToManyField(User, blank=True, related_name="online_groups")
    moderators = models.ManyToManyField(User, blank=True, related_name="moderated_groups")

    def __str__(self):
        return self.group_name


class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, related_name="messages")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"[{self.created.strftime('%Y-%m-%d %H:%M:%S')}] {self.group.group_name} - {self.author.username}: {self.body}"


class Friend(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="friend_profile")

    def __str__(self):
        return f"{self.user.username}'s Friend List"


class Friendship(models.Model):
    from_user = models.ForeignKey(User, related_name="friendships_sent", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="friendships_received", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user.username} ↔ {self.to_user.username}"


class PrivateMessage(GroupMessage):
    friend = models.ForeignKey(Friend, on_delete=models.CASCADE, related_name="private_messages")

    def __str__(self):
        return f"Private to {self.friend.user.username}: {self.body}"
