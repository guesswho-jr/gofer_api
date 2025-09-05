from rest_framework import generics
from rest_framework.response import Response
from Gofer_main.classes import GoferListCreateView
from story.serializers import StoryCreateUpdateSerializer, StorySerializer

from .models import Story
from django.utils import timezone
class StoryListCreateView(GoferListCreateView):
    queryset = Story.objects.filter(created_at__gt = timezone.now() - timezone.timedelta(days=1))
    def get_serializer_class(self): # type: ignore
        if self.request.method == "GET":
            return StorySerializer
        else: 
            return StoryCreateUpdateSerializer
    def perform_create(self, serializer):
        serializer.save()
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            return Response({
                "success": True
            }, status=201)
class StoryRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Story.objects.filter(created_at__gt = timezone.now() - timezone.timedelta(days=1))
    # serializer_class = StorySerializerList
    lookup_field = 'id'
    def get_serializer_class(self): # type: ignore
        if self.request.method in ["PUT", "PATCH"]:
            return StoryCreateUpdateSerializer
        return StorySerializer

