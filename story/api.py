from django.utils import timezone
from story.models import Story
from .serializers import StorySerializer
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async

async def get_all_stories(filter_for_user = None):
    expiration_time = timezone.now() - timezone.timedelta(hours=24)
    data = await sync_to_async(Story.objects.filter)(created_at__gt=expiration_time)
    if filter_for_user:
        User = get_user_model()
        u = User.objects.get(username = filter_for_user)
        if u:
            data = await sync_to_async(data.filter)(uploaded_by=u)
    stories = []
    for story in data:
        serializer = StorySerializer(data=story)
        stories.append(await serializer.adata) # type: ignore
    return stories