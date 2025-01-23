from django.urls import path
from rest_framework.routers import DefaultRouter
from main.api.friendship import ListFriendshipView, RejectFriendRequestView, ListCreateFriendRequestsView, AcceptFriendRequestView, RemoveFriendView

urlpatterns = [
    path("", ListFriendshipView.as_view(), name="friendship"),
    path("requests/", ListCreateFriendRequestsView.as_view(), name="friend_requests"),
    path("accept/<int:pk>/", AcceptFriendRequestView.as_view(), name="accept_friend_request"),
    path("reject/<int:pk>/", RejectFriendRequestView.as_view(), name="reject_friend_request"),
    path("remove/<int:pk>/", RemoveFriendView.as_view(), name="remove_friend"),
]