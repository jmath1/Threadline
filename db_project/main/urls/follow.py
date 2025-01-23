from django.urls import path
from main.api.follow import FollowViewSet
urlpatterns = [
    path("followers/", FollowViewSet.as_view({"get": "list_followers"}), name="followers"),
    path("following/", FollowViewSet.as_view({"get": "list_following"}), name="following"),
    path("<int:followee_id>/", FollowViewSet.as_view({"post": "follow"}), name="follow"),
    path("unfollow/<int:followee_id>", FollowViewSet.as_view({"post": "unfollow"}), name="unfollow"),
]