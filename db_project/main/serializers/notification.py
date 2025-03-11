from rest_framework import serializers


class NotificationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    type = serializers.CharField(max_length=100)
    thread_id = serializers.IntegerField()
    message_id = serializers.IntegerField()
    friendship_id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    status = serializers.CharField(max_length=100)

    def create(self, validated_data):
        # Implement create logic if needed (for notifications created from the API)
        return validated_data

    def update(self, instance, validated_data):
        # Implement update logic if needed
        pass