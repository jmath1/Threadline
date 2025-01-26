from main.models import Notification
from rest_framework.serializers import ModelSerializer


class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = ["user_id", "type", "thread_id", "message_id", "friendship_id", "message", "created_at", "updated_at", "status"]
        read_only_fields = ["user_id", "type", "thread_id", "message_id", "friendship_id," "message", "created_at", "updated_at"]