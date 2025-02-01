from main.models import Hood, Message, Tag, Thread, User

from main.serializers.user import UserSerializer
from rest_framework import serializers

def handle_tags(author, thread, message):
    """
    Parse message content for tags (e.g., '@username') and add tagged users as participants.
    """
    # Parse tags from the message. Only include friends of author
    message_content = message.content
    tagged_usernames = {word[1:] for word in message_content.split() if word.startswith('@')}
    tagged_users = author.get_friends().filter(username__in=tagged_usernames)

    # Add tagged users to the thread participants
    for user in tagged_users:
        thread.participants.add(user)
        message.tags.append(Tag(
            user_id=user.id,
            username=user.username
        ))

    # Add the author to the thread participants
    thread.participants.add(author)
    thread.save()
    message.save()

class TagSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    username = serializers.CharField()

    def to_representation(self, instance):
        return {
            "user_id": instance.user_id,
            "username": instance.username
        }

    def to_internal_value(self, data):
        return User.objects.get(id=data)
    
class MessageSerializer(serializers.Serializer):
    external_id = serializers.CharField(read_only=True)
    thread_id = serializers.CharField(write_only=True)
    author_id = serializers.CharField()
    content = serializers.CharField(max_length=1000)
    tags = serializers.ListField(
        child=TagSerializer(),
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
        # try:
        message = Message(**validated_data).save()
        handle_tags(thread=Thread.objects.get(id=validated_data["thread_id"]), author=self.context['request'].user, message=message)
        # except Exception as exc:
        #     import pdb; pdb.set_trace()
        #     raise serializers.ValidationError("Failed to create message.")
        return message

    def update(self, instance, validated_data):
        # Update the MongoDB document
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        handle_tags(thread=Thread.objects.get(id=instance.thread_id), author=self.context['request'].user, message=instance)
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

            handle_tags(self.context["request"].user, thread, message)
            return thread
        except Exception as e:
            # Log or handle the exception as needed
            thread.delete()
            raise serializers.ValidationError(f"Failed to create thread: {e}")


