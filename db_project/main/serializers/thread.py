from django.db import transaction
from main.models import Hood, Message, Thread, User
from main.serializers.user import UserSerializer
from rest_framework import serializers


class MessageSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    thread_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Message
        fields = ["content", "author", "created_at", "updated_at", "thread_id"]

    def create(self, validated_data):
        if not validated_data.get("thread_id"):
            raise serializers.ValidationError("Thread ID is required.")
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)

class ThreadSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    type = serializers.CharField(max_length=10)
    hood = serializers.PrimaryKeyRelatedField(queryset=Hood.objects.all())
    participants = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    created_at = serializers.DateTimeField()
    author = UserSerializer()
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Thread
        fields = ["name", "type", "hood", "participants", "author", "created_at", "messages"]
        read_only_fields = ["created_at", "messages"]

class CreateThreadSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    type = serializers.CharField(max_length=10)
    hood = serializers.PrimaryKeyRelatedField(queryset=Hood.objects.all(), required=False)
    participants = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    content = serializers.CharField(max_length=500)
    
    class Meta:
        fields = ["name", "type", "hood", "participants", "content"]
    
    def save(self, **kwargs):
        try:
            with transaction.atomic():
                # Create the thread
                thread = Thread.objects.create(
                    name=self.validated_data["name"],
                    type=self.validated_data["type"],
                    hood=self.validated_data.get("hood"),
                    author=self.context["request"].user
                )

                # Create the initial message
                message = Message.objects.create(
                    thread=thread,
                    author=self.context["request"].user,
                    content=self.validated_data["content"]
                )

                # Handle tagged users and add participants
                self._handle_tags(self.context["request"].user, thread, message.content)

                return thread
        except Exception as e:
            # Log or handle the exception as needed
            raise serializers.ValidationError(f"Failed to create thread: {e}")

    def _handle_tags(self, author, thread, message_content):
        """
        Parse message content for tags (e.g., '@username') and add tagged users as participants.
        """
        # Parse tags from the message
        tagged_usernames = {word[1:] for word in message_content.split() if word.startswith('@')}
        tagged_users = User.objects.filter(username__in=tagged_usernames)

        # Add tagged users to the thread participants
        for user in tagged_users:
            thread.participants.add(user)

        # Add the author to the thread participants
        thread.participants.add(author)
        thread.save()
