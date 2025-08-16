from adrf import generics

from rest_framework.response import Response
from accounts.models import Provider, User, UserProfile
from accounts.serializers import UserDetailSerializer



class UserGetView(generics.RetrieveAPIView):
    parent_queryset = User.objects.all()
    profile_queryset = UserProfile.objects.all()
    provider_queryset = Provider.objects.all()
    serializer_class = UserDetailSerializer
    async def get(self, request, *args, **kwargs):
        username = kwargs.get("username")
        u = await User.objects.aget(username=username)
        user_profile = await UserProfile.objects.aget(user=u)
        return Response(user_profile.profile_picture)
        # return super().get(request, *args, **kwargs)

