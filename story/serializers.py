from rest_framework.serializers import ModelSerializer
from .models import Story

class StorySerializer(ModelSerializer):
    class Meta:
        model = Story
        fields = [
            "story_image",
            "id",
            "caption",
            "posted_at",
            "posted_by",
            "poster_image"
        ]
        