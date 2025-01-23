from django.urls import path
from main.api import user as api

urlpatterns = [
    path("register/", api.UserRegisterView.as_view()),
    path("<int:user_id>/", api.GetUserDetail.as_view()),
    path("me/", api.MeGET.as_view()),
    #path("login/", api.UserLogin.as_view()),
    path("edit/", api.EditUserView.as_view()),
    # path("user/<int:user_id>/threads/", api.GetUserThreads.as_view()),
    path("neighbors/", api.GetNeighborList.as_view()),
        
]
