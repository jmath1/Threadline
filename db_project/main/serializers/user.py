import os

import requests
from django.contrib.gis.geos import Point
from main.models import Hood, User
from main.utils.utils import process_coords
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class PointField(serializers.Field):
    def to_representation(self, value):
        if value:
            return value.coords
        return None

    def to_internal_value(self, data, **kwargs):
        
        return Point(data[0], data[1], geography=True, srid=4326)

class UserSerializer(GeoFeatureModelSerializer):
    username = serializers.CharField(max_length=50)
    first_name = serializers.RegexField(regex=r'^[a-zA-Z0-9]*$', max_length=50)
    last_name = serializers.RegexField(regex=r'^[a-zA-Z0-9]*$', max_length=50)
    email = serializers.CharField(max_length=25)
    photo_url = serializers.CharField(max_length=255, required=False, allow_null=True)
    address = serializers.CharField(max_length=255)   
    coords = PointField(required=False, allow_null=True, default=None)
    password = serializers.CharField(max_length=30, write_only=True)
    
    class Meta:
        model = User
        geo_field = "coords"
        fields = [
            "username", "first_name", "last_name", "email", "password", "hood", "photo_url", "address", "coords"
        ]

class MeSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    first_name = serializers.RegexField(regex=r'^[a-zA-Z0-9]*$', max_length=50)
    last_name = serializers.RegexField(regex=r'^[a-zA-Z0-9]*$', max_length=50)
    email = serializers.CharField(max_length=25)
    photo_url = serializers.CharField(max_length=255, required=False, allow_null=True)
    address = serializers.CharField(max_length=255)   
    coords = PointField(required=False)
    hood = serializers.PrimaryKeyRelatedField(queryset=Hood.objects.all(), required=False)
    followers_count = serializers.IntegerField()
    following_count = serializers.IntegerField()
    friends_count = serializers.IntegerField()
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["neighborhood"] = instance.hood.name,
        return data
        
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=30)
    
class EditUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50, required=False)
    password = serializers.CharField(max_length=30, required=False)
    first_name = serializers.RegexField(regex=r'^[a-zA-Z0-9]*$', max_length=50, required=False)
    last_name = serializers.RegexField(regex=r'^[a-zA-Z0-9]*$', max_length=50,required=False)
    email = serializers.CharField(max_length=25,required=False)
    photo_url = serializers.CharField(max_length=255, required=False, allow_null=True)
    address = serializers.CharField(max_length=200, required=False)
    
    class Meta:
        model = User
        fields = ["username", "password", "first_name", "last_name", "email", "photo_url", "address"]
        
    def validate_address(self, value):
        hood, coords = process_coords(value)
        if not hood:
            raise ValidationError("Hood not supported")
        return value
    
    def update(self, instance, validated_data):
        data = self.validated_data
        if "address" in data:
            hood, coords = process_coords(data["address"])
            data["hood"] = hood
            data["coords"] = coords
        for key, value in data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
