import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.humanize.templatetags.humanize import naturaltime

User = get_user_model()
class Story(models.Model):
    id = models.UUIDField(editable=False, unique=True, primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.CharField(max_length=1024)
    image = models.ImageField(upload_to='stories/%Y/%m/%d/', null=False, blank=False) # change to imagefield
    
    def __str__(self):
        return self.uploaded_by.username
    @property
    def posted_at(self):
        return naturaltime(self.created_at)
    @property
    def posted_by(self):
        return self.uploaded_by.username
    @property
    def story_image(self):
        return self.image.url
    @property
    def poster_image(self):
        return self.uploaded_by.profile.profile_picture.url # type: ignore
    
    class Meta:
        verbose_name_plural = "Stories"