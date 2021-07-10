from django.db import models
from django.core.cache import cache 
import datetime
from Chat import settings

# Create your models here.
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user   = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.FileField(upload_to="Profile")

    def last_seen(self):
        return cache.get('seen_%s' % self.user.username)

    def online(self):
        
        if self.last_seen():
            now = datetime.datetime.now()
            if now > self.last_seen() + datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT):
                return 0
            else:
                return 1
        else:
            return 0 

