from rest_framework import serializers
from adrf.serializers import Serializer

from accounts.models import UserProfile



class RegisterSerializer(serializers.Serializer):
    user_type = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()
    cpassword = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    location = serializers.JSONField(required=False)
    # profile_picture = serializers.ImageField()
class LoginSerializerAsync(serializers.ModelSerializer):
    class Meta:
        fields = ['username', 'password']
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', "email", "full_name")