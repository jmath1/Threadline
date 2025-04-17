from django.urls import path
from main.api import user as api

urlpatterns = [
    path("register/", api.UserRegisterView.as_view()),
    path("<int:pk>/", api.GetUserDetail.as_view()),
    path("me/", api.MeGET.as_view()),
    #path("login/", api.UserLogin.as_view()),
    path("edit/", api.EditUserView.as_view()),
    path("new-members/", api.NewlyJoinedMembers.as_view()),
]
