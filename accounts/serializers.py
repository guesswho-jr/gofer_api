import json
from typing import Dict
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from accounts.models import User, UserProfile

from django.core.exceptions import ValidationError
from Gofer_main.exceptions import BadRequest
from utils.json_schemas import validate_follows_schema, validate_location_schema

class RegisterSerializer(serializers.Serializer):
    user_type = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()
    cpassword = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    location = serializers.JSONField(required=False, validators=[validate_location_schema])
    # profile_picture = serializers.ImageField()
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
class UserDetailSerializer(serializers.ModelSerializer):
    # full_name = serializers.CharField()
    follows = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('username', "email", "follows")
    def get_follows(self, obj):
        usernames = []
        if (isinstance(obj, User)):
            if (hasattr(obj, "follows")):
                # print(obj.follows.all())
                for user in list(obj.follows.all()): # type: ignore
                    # print(user.follows)
                    # username = get_object_or_404(User, id=user.follows.id).username
                    # username = User.objects.get(pk=user.id).username
                    usernames.append(user.follows.username)
                                       
            else:
                return []
        else:
            print("Error in here no User")
            return []
        return usernames
        # def get_full_name(self):
        #     return 'test'
class UserProfileDetailSerializer(serializers.ModelSerializer):
    # full_name = serializers.CharField()
    class Meta:
        model = UserProfile
        fields = ('full_name', "profilePicture", "is_provider" , "settings")
        
        # def get_full_name(self):
        #     return 'test'

class UserUpdateSerializer(serializers.ModelSerializer):
    cpassword = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    follows = serializers.JSONField(required=False, validators=[validate_follows_schema])
    user_type = serializers.CharField(required=False)
    location = serializers.JSONField(required=False, validators=[validate_location_schema])
    class Meta:
        model = User
        fields = ("username", "password", "email", "first_name", "last_name", "cpassword", "follows", "user_type", "location")
    
    def validate(self, attrs):
        if "password" in attrs.keys():
            if not ("cpassword" in attrs.keys()):
                raise BadRequest("Please input the password again for confirmation.")
            if attrs["password"] != attrs["cpassword"]:
                raise ValidationError("Passwords don't match")
            attrs.pop("cpassword")
        if "user_type" in attrs.keys():
            user_type = attrs.get("user_type") 
            if not user_type in ["provider", "user"]:
                raise ValidationError("Not a valid data")
            if "location" not in attrs.keys():
                raise BadRequest("Location is required if you are a provider.")
        return attrs
        