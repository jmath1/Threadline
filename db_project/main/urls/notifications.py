from django.urls import path
from main.api.notification import (MarkNotificationReadAPIView,
                                   NotificationListAPIView)

urlpatterns = [
    path("", NotificationListAPIView.as_view()),
    path("<int:pk>/read/", MarkNotificationReadAPIView.as_view()),
]