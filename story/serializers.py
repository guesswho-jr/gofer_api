from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from Gofer_main.exception_classes import UnknownException
from .models import Story, User

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
class StoryCreateUpdateSerializer(ModelSerializer):
    username = serializers.CharField()
    class Meta:
        model = Story
        fields = ("caption", "image", "username")
    def create(self, validated_data: dict):
        username = validated_data.pop("username")
        try: 
            u = User.objects.get(username=username)
            
        except User.DoesNotExist: 
            raise ValidationError("The user you requested does not exist. ", "user_not_found")
        except Exception as e:
            raise UnknownException(e)
        return Story.objects.create(**validated_data, uploaded_by=u)
    def update(self, instance, validated_data: dict):
        username = validated_data.pop("username")
        try: 
            u = User.objects.get(username=username)
        except User.DoesNotExist: 
            raise ValidationError("The user you requested does not exist. ", "user_not_found")
        except Exception as e:
            raise UnknownException(e)
        return super().update(instance, {**validated_data, "uploaded_by":u})
        