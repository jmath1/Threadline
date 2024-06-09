from django.urls import path
from main.api import user as api

urlpatterns = [
    path("register/", api.ProfileRegisterView.as_view()),
    path("<int:user_id>/", api.GetUserDetail.as_view()),
    path("me/", api.MeGET.as_view()),
    path("login/", api.ProfileLogin.as_view()),
    path("edit/", api.EditProfileView.as_view()),
    # path("user/<int:user_id>/threads/", api.GetUserThreads.as_view()),
    path("followers/", api.GetFollowers.as_view()),  
    path("following/", api.GetFollowing.as_view()),
    path("friends/", api.GetFriendsList.as_view()),
    path("neighbors/", api.GetNeighborList.as_view()),
    path('add-friend/', api.AddFriendView.as_view(), name='add-friend'),
    path('delete-friend/', api.DeleteFriendView.as_view(), name='delete-friend'),
    path('delete-follower/', api.DeleteFollowerView.as_view(), name='delete-follower'),
    path('follow/', api.FollowView.as_view(), name='follow'),
    path('confirm-friend/', api.AcceptFriendshipView.as_view(), name='accept-friendship'),
    path('decline-friend/', api.DeclineFriendshipView.as_view(), name='decline-friendship'),
    path('friendship-requests/', api.FriendshipRequestsView.as_view(), name='friendship-requests'),

        
]
