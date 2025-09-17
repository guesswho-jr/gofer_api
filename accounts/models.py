import json
from django.db import models
from django.contrib.auth import get_user_model

from utils.json_schemas import default_settings, validate_location_schema, validate_settings_schema


User = get_user_model()
class UserProfile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name="profile")
    profile_picture = models.ImageField(upload_to="profilePictures/", blank=True)
    settings = models.JSONField(default=default_settings, validators=[validate_settings_schema])
    # follows = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="follows",  blank=True)
    def __str__(self):
        return self.user.username
    @property
    def is_provider(self):
        return hasattr(self, "provider")
    @property
    def profilePicture(self):
        return self.profile_picture.url
    @property
    def full_name(self):
        return self.user.first_name + ' ' + self.user.last_name
    
class Provider(models.Model):
    user_profile = models.OneToOneField(to=UserProfile, on_delete=models.CASCADE, related_name="provider")
    location = models.JSONField(validators=[validate_location_schema])
    def __str__(self) -> str:
        return self.user_profile.user.username

class Social(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="follows")
    follows = models.ForeignKey(to=User, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return f"{self.user.username} follows {self.follows.username}"