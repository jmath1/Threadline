from rest_framework import serializers

from main.models import Follow, User

class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]
        
        
    
class FollowSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Follow
        fields = ["follower_id", "followee_id"]
        read_only_fields = ["created_at"]
        
    def create(self, validated_data):
        return Follow.objects.create(
            follower_id=validated_data["follower"]["id"],
            followee_id=validated_data["followee"]["id"]
        )
        
    def update(self, instance, validated_data):
        instance.follower_id = validated_data["follower"]["id"]
        instance.followee_id = validated_data["followee"]["id"]
        instance.save()
        return instance
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["follower"] = instance.follower.username
        ret["followee"] = instance.followee.username
        return ret
    
    def to_internal_value(self, data):
        return {
            "follower": data["follower"]["id"],
            "followee": data["followee"]["id"]
        }