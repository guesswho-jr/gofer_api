from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
class UserProfile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to="profilePictures/", null=False)
    def __str__(self):
        return self.user.username