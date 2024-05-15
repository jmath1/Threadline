from django.urls import path

from main.api import block as api

urlpatterns = [
    path("block/<int:block_id>/threads/", api.GetBlockThreads.as_view()),
    path("block/<int:block_id>/members/", api.ListBlockMembers.as_view()),
    path("block/follows/", api.GetBlockFollows.as_view()),
]