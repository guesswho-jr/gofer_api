import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
class Story(models.Model):
    id = models.UUIDField(editable=False, unique=True, primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.OneToOneField(User, on_delete=models.CASCADE)
    caption = models.CharField(max_length=1024)
    image = models.ImageField(upload_to='stories/%Y/%m/%d/', null=True) # change to imagefield
    
    def __str__(self):
        return self.uploaded_by.username
    
    class Meta:
        verbose_name_plural = "Stories"