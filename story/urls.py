from django.urls import path

from story.views import StoryListCreateView, StoryRetrieveUpdateView
urlpatterns = [
    path("", StoryListCreateView.as_view()),
    # path("create/", StoryCreateView.as_view()),
    path("<str:id>/", StoryRetrieveUpdateView.as_view()),
]