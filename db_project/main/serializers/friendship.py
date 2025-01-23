from rest_framework import serializers
from main.models import Friendship, User
from main.constants import FRIEND_REQUEST_STATUS_CHOICES
from django.shortcuts import get_object_or_404

class FriendshipRequestSerializer(serializers.ModelSerializer):
    from_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    to_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    status = serializers.CharField(max_length=255, default="REQUESTED")
    
    class Meta:
        model = Friendship
        fields = ["from_user", "to_user", "status", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at", "from_user", "to_user"]
    
    def to_representation(self, instance):
        repr =  super().to_representation(instance)
        repr["from_user"] = {
            "username": instance.from_user.username,
            "id": instance.from_user.id,
        }
        repr["to_user"] = {
            "username": instance.to_user.username,
            "id": instance.to_user.id,
        }
        return repr
    
