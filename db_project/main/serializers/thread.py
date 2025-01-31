from django.db import transaction
from main.models import Hood, Message, Thread, User
from main.serializers.user import UserSerializer
from rest_framework import serializers


class MessageSerializer(serializers.Serializer):
    external_id = serializers.CharField(read_only=True)
    thread_id = serializers.CharField(write_only=True)
    author_id = serializers.CharField()
    content = serializers.CharField(max_length=1000)
    tags = serializers.ListField(
        child=serializers.IntegerField(),  # List of User IDs
        required=False
    )
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def validate_tags(self, tags):
        # Ensure all tag IDs exist in the PostgreSQL User table
        missing_users = [tag for tag in tags if not User.objects.filter(id=tag).exists()]
        if missing_users:
            raise serializers.ValidationError(f"Invalid user IDs: {missing_users}")
        return tags
    
    def validate_thread_id(self, thread_id):
        # Ensure the thread ID exists in the PostgreSQL Thread table
        if not Thread.objects.filter(id=thread_id).exists():
            raise serializers.ValidationError("Invalid thread ID.")
        return thread_id

    def create(self, validated_data):
        # Save to MongoDB
        return Message(**validated_data).save()

    def update(self, instance, validated_data):
        # Update the MongoDB document
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance
    


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
        thread = Thread.objects.create(
            name=self.validated_data["name"],
            type=self.validated_data["type"],
            hood=self.validated_data.get("hood"),
            author=self.context["request"].user
        )

        try:
            message = Message.objects.create(
                thread_id=thread.id,
                author_id=self.context["request"].user.id,
                content=self.validated_data["content"]
            )

            self._handle_tags(self.context["request"].user, thread, message.content)
            return thread
        except Exception as e:
            # Log or handle the exception as needed
            thread.delete()
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
