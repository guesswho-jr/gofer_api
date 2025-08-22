from django.shortcuts import get_object_or_404
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
        fields = ('full_name', "profilePicture", "is_provider")
        
        # def get_full_name(self):
        #     return 'test'
