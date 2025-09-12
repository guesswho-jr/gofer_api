from rest_framework import generics

from rest_framework.response import Response
from accounts.models import Provider, User, UserProfile
from accounts.serializers import UserDetailSerializer, UserProfileDetailSerializer
from dashboard.models import Product
from dashboard.serializer import ProductListSerailizer



class UserGetView(generics.RetrieveAPIView):
    parent_queryset = User.objects.all()
    profile_queryset = UserProfile.objects.all()
    serializer_class_for_profile = UserProfileDetailSerializer
    serializer_class_for_user = UserDetailSerializer
    def get(self, request, *args, **kwargs):
        username = kwargs.get("username")
        u =  User.objects.get(username=username)
        user_profile =  UserProfile.objects.get(user=u)
        user_data = dict(self.serializer_class_for_profile(user_profile).data)
        user_profile_data = dict(self.serializer_class_for_user(u).data)
        
        user_data_data = {**user_data, **user_profile_data}
        return Response(user_data_data)

# Next up: Paging
