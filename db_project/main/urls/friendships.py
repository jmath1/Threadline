from django.urls import path
from main.api.friendship import (AcceptFriendRequestView,
                                 ListCreateFriendRequestsView,
                                 ListFriendshipView, RejectFriendRequestView,
                                 RemoveFriendView)
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path("", ListFriendshipView.as_view(), name="friendship"),
    path("requests/", ListCreateFriendRequestsView.as_view(), name="friend_requests"),
    path("accept/<int:pk>/", AcceptFriendRequestView.as_view(), name="accept_friend_request"),
    path("reject/<int:pk>/", RejectFriendRequestView.as_view(), name="reject_friend_request"),
    path("remove/<int:pk>/", RemoveFriendView.as_view(), name="remove_friend"),
]