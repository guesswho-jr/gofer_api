from rest_framework import generics

from story.serializers import StorySerializer

from .models import Story
from django.utils import timezone

class StoryListView(generics.ListAPIView):
    queryset = Story.objects.filter(created_at__gt = timezone.now() - timezone.timedelta(days=1))
    serializer_class = StorySerializer
    
class StoryRetrieveView(generics.RetrieveAPIView):
    queryset = Story.objects.filter(created_at__gt = timezone.now() - timezone.timedelta(days=1))
    serializer_class = StorySerializer
    lookup_field = 'id'

class StoryCreateView(generics.CreateAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    def perform_create(self, serializer):
        serializer.save()
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            return Response({
                "success": True
            }, status=201)
