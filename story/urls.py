from django.urls import path

from story.views import StoryListView, StoryRetrieveUpdateView, StoryCreateView
urlpatterns = [
    path("", StoryListView.as_view()),
    path("create/", StoryCreateView.as_view()),
    path("<str:id>/", StoryRetrieveUpdateView.as_view()),
]