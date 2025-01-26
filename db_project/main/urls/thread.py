from django.urls import path
from main.api import thread as api

urlpatterns = [    
    path("<int:pk>/", api.RetrieveDestroyThread.as_view()),
    path("", api.CreateThread.as_view()),
    
    # # follow/unfollow
    # path("<int:thread_id>/follow/", api.FollowThread.as_view()),
    # path("<int:thread_id>/unfollow/", api.UnfollowThread.as_view()),
    # path("<int:thread_id>/members/", api.ListThreadMembers.as_view()),
    # path("<int:thread_id>/messages/", api.ListThreadMessages.as_view()),
    
    # # edit delete messages
    # path("message/<int:message_id>/edit/", api.EditDeleteMessage.as_view()),
    # path("message/<int:message_id>/delete/", api.DeleteMessage.as_view()),
    # path("message/<int:thread_id>/create/", api.CreateMessage.as_view()),
    # path("search/", api.ThreadSearchView.as_view()),


    # # # feeds for newest
    # # path("hood/newest/", api.GetNewHoodThreads.as_view()),
    # # path("user/newest/", api.GetNewUserThreads.as_view()),
    
    # # # general, not newest
    # path("user/", api.GetUserThreads.as_view()),
    # path("hood/", api.GetHoodThreads.as_view()),
]
