from rest_framework.serializers import ModelSerializer
from main.models import Notification

class NotificationSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = ["user_id", "notification_type", "thread_id", "message_id", "friendship_id," "message", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]