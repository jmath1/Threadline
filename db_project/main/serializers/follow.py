from main.models import User
from rest_framework import serializers


class FollowerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]
        
        