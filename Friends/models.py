from django.db import models
from django.contrib.auth.models import User

FRIENDS_STATUS=(
    ('1', "pending"),
    ('2', "accepted")
)

class FriendsOfFriends(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendship_requests_sent')
    friends = models.ForeignKey(User,on_delete=models.CASCADE, related_name='friendship_requests_received')
    status = models.CharField(max_length=20, choices=FRIENDS_STATUS)
    
    def __str__(self):
        return self.user.username+","+ self.friends.username+","+self.status
    
    class Meta:
        unique_together=(('user', 'friends'),)