from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
class UserProfile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name="profile")
    profile_picture = models.ImageField(upload_to="profilePictures/")
    def __str__(self):
        return self.user.username
    @property
    def is_provider(self):
        return hasattr(self, "provider")
    @property
    def profilePicture(self):
        return self.profile_picture.url
class Provider(models.Model):
    user_profile = models.OneToOneField(to=UserProfile, on_delete=models.CASCADE, related_name="provider")
    location = models.JSONField(null=True, blank=True)
    def __str__(self) -> str:
        return self.user_profile.user.username
    