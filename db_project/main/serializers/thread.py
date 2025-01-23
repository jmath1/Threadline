from rest_framework import serializers
from main.models import Thread, Message

class MessageSerializer(serializers.ModelSerializer):
    body = serializers.CharField(max_length=255)
    user_id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    
    class Meta:
        model = Message
        fields = ["body", "user_id", "created_at", "updated_at"]

class ThreadSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255)
    body = serializers.CharField(max_length=255)
    user_id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    
    #messages are from a message serializer
    messages = MessageSerializer(many=True)
    
    class Meta:
        model = Thread
        fields = ["title", "body", "user_id", "created_at", "updated_at", "messages"]
        read_only_fields = ["created_at", "updated_at", "messages"]