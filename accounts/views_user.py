from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.response import Response
from Gofer_main.classes import GoferBaseView
from accounts.lib.user_update import handle_update
from accounts.models import Provider, Social, User, UserProfile
from accounts.serializers import UserDetailSerializer, UserProfileDetailSerializer, UserUpdateSerializer
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError, APIException
class UserGetView(GoferBaseView):
    parent_queryset = User.objects.all()
    profile_queryset = UserProfile.objects.all()
    serializer_class_for_profile = UserProfileDetailSerializer
    serializer_class_for_user = UserDetailSerializer
    # for the generic view
    update_serializer_class = UserUpdateSerializer
    def unpack_users(self,username):
        u =  User.objects.get(username=username)
        user_profile =  UserProfile.objects.get(user=u)
        return u, user_profile
    def get(self, request, *args, **kwargs):
        username = kwargs.get("username")
        # username = kwargs.get("username")
        user, user_profile = self.unpack_users(username)
        user_data = dict(self.serializer_class_for_profile(user_profile).data)
        user_profile_data = dict(self.serializer_class_for_user(user).data)
        
        user_data_data = {**user_data, **user_profile_data}
        return Response(user_data_data)
    def post(self, request, *args, **kwargs):
        serializer = self.update_serializer_class(data=request.data)
        # print(request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        if not type(data) == ReturnDict:
            raise ValidationError(detail="Invalid data received", code="invalid")
        
        username = self.get_user_from_token()
        user = get_object_or_404(User, username=username)
        handle_update(data, user)
        return Response({"success": True})
# Next up: Paging
