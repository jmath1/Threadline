from django.urls import path

from main.api import hood

urlpatterns = [
    path("<int:hood_id>/members/", hood.ListHoodMembers.as_view()),
    path("follows/", hood.GetHoodFollows.as_view()),
    
]
    