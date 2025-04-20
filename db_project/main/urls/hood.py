from django.urls import path
from main.api import hood

urlpatterns = [
    path("", hood.ListHoods.as_view()),
    path("<int:pk>/members/", hood.ListHoodMembers.as_view()),
    path("<int:pk>/followers/", hood.GetHoodFollowers.as_view()),
    path("followed/", hood.GetUserHoodsFollowed.as_view()),
]
    