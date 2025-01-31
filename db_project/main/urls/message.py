from django.urls import path
from main.api import message as api

urlpatterns = [
    path("", api.CreateMessage.as_view()),
    path("<str:external_id>/", api.UpdateDestroyMessage.as_view()),
]