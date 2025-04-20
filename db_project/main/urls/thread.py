from django.urls import path
from main.api import thread as api

urlpatterns = [    
    path("<int:pk>/", api.RetrieveDestroyThread.as_view()),
    path("", api.CreateThread.as_view()),
    path("hood/<int:hood_id>/", api.GetHoodThreads.as_view()),
    
    # # follow/unfollow
    path("<int:thread_id>/follow/", api.FollowThread.as_view()),
    path("<int:thread_id>/unfollow/", api.UnfollowThread.as_view()),
    path("recently-created/", api.GetRecentlyCreatedThreads.as_view()),
    path("new-messages/", api.GetThreadsWithNewMessages.as_view()),
]
