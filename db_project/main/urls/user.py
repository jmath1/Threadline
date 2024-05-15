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
        
]
