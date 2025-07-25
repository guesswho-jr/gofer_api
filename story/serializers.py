from adrf.serializers import ModelSerializer, Serializer
from rest_framework import serializers as srl
from .models import Story

class StorySerializer(ModelSerializer):
    class Meta:
        model = Story
        fields = [
    "id",
    "upload_date",
    "uploaded_by",
    "caption",
    "image"
        ]