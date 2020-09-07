from django.db import models
from django.contrib.auth.models import User
from annoying.fields import AutoOneToOneField

# Create your models here.
class UserProfilePic(models.Model):
    user = AutoOneToOneField(User, on_delete=models.CASCADE, null=True)
    profile_pic = models.ImageField(default='profile_pictures/avatar.png', upload_to='profile_pictures')

    def __str__(self):
        return str(self.user)