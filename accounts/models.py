from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
class UserProfile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name="profile")
    profile_picture = models.ImageField(upload_to="profilePictures/")
    def __str__(self):
        return self.user.username