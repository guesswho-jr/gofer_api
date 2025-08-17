from rest_framework import serializers

from accounts.models import User, UserProfile



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
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
class UserDetailSerializer(serializers.ModelSerializer):
    # full_name = serializers.CharField()
    class Meta:
        model = User
        fields = ('username', "email")
        
        # def get_full_name(self):
        #     return 'test'
class UserProfileDetailSerializer(serializers.ModelSerializer):
    # full_name = serializers.CharField()
    class Meta:
        model = UserProfile
        fields = ('full_name', "profilePicture", "is_provider")
        
        # def get_full_name(self):
        #     return 'test'
