from django.urls import path

from story.views import StoryListView, StoryRetrieveView, StoryCreateView
urlpatterns = [
    path("", StoryListView.as_view()),
    path("create/", StoryCreateView.as_view()),
    path("<str:id>", StoryRetrieveView.as_view()),
]