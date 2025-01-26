from main.models import Hood
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


class HoodSerializer(ModelSerializer):
    member_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Hood
        fields = ["id", "name", "member_count"]