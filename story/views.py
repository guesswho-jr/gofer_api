from rest_framework import generics
from rest_framework.response import Response
from story.serializers import StoryCreateUpdateSerializer, StorySerializer
from rest_framework.pagination import PageNumberPagination
from .models import Story, User
from django.utils import timezone
from rest_framework_simplejwt.tokens import AccessToken
class StoryListView(generics.ListAPIView):
    serializer_class = StorySerializer
    pagination_class = PageNumberPagination
    def get_user_from_token(self):
        raw_token = self.request.headers["Authorization"].split(" ")[1]
        t = AccessToken(raw_token)
        user = User.objects.get(pk=t["user_id"])
        return user
    def get_queryset(self): # type: ignore
        story_wanter = self.get_user_from_token()
        pre_follow_list = story_wanter.follows.all()
        follow_list = map(lambda x: x.follows, pre_follow_list)
        data = Story.objects.filter(created_at__gt = timezone.now() - timezone.timedelta(days=1)).exclude(uploaded_by=story_wanter)
        data = data.filter(uploaded_by__in=follow_list)
        return data
        # return super().get_queryset()
    
class StoryRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Story.objects.filter(created_at__gt = timezone.now() - timezone.timedelta(days=1))
    # serializer_class = StorySerializerList
    lookup_field = 'id'
    def get_serializer_class(self): # type: ignore
        if self.request.method in ["PUT", "PATCH"]:
            return StoryCreateUpdateSerializer
        return StorySerializer

class StoryCreateView(generics.CreateAPIView):
    queryset = Story.objects.all()
    serializer_class = StoryCreateUpdateSerializer
    def perform_create(self, serializer):
        serializer.save()
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            return Response({
                "success": True
            }, status=201)
