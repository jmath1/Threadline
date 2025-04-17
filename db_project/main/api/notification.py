import json

import redis
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from main.serializers.general import EmptySerializer
from main.serializers.notification import NotificationSerializer
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


class NotificationListAPIView(ListAPIView):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        """
        Get notifications for the current user from Redis.
        """
        user_id = self.request.user.id
        notifications_key = f"notifications:user:{user_id}"
        notifications = redis_client.lrange(notifications_key, 0, -1)
        notifications_data = [json.loads(notification) for notification in notifications]
        
        return notifications_data

class MarkNotificationReadAPIView(GenericAPIView):
    serializer_class = EmptySerializer

    def get_queryset(self):
        return None
    def get_object(self):
        user_id = self.request.user.id
        notification_id = self.kwargs["notification_id"]
        notifications_key = f"notifications:user:{user_id}"
        notifications = redis_client.lrange(notifications_key, 0, -1)
        for notification in notifications:
            notification_data = json.loads(notification)
            if notification_data["id"] == notification_id:
                return notification_data
        return None
    
    @swagger_auto_schema(
        operation_description="Mark a notification as read",
        responses={200: NotificationSerializer},
    )
    def put(self, request, *args, **kwargs):
        notification = self.get_object()
        if notification:
            notification["read"] = True
            user_id = self.request.user.id
            notifications_key = f"notifications:user:{user_id}"
            notifications = redis_client.lrange(notifications_key, 0, -1)
            for index, notif in enumerate(notifications):
                notif_data = json.loads(notif)
                if notif_data["id"] == notification["id"]:
                    redis_client.lset(notifications_key, index, json.dumps(notification))
                    break
        return Response(NotificationSerializer(notification).data)
        
        