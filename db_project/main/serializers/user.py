import os

import requests
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from main.models import Hood, User
from django.contrib.gis.geos import Point

from rest_framework_gis.serializers import GeoFeatureModelSerializer

class PointField(serializers.Field):
    def to_representation(self, value):
        return value.coords

    def to_internal_value(self, data, **kwargs):
        
        return Point(data[0], data[1], geography=True, srid=4326)

class UserSerializer(GeoFeatureModelSerializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=30)
    first_name = serializers.RegexField(regex=r'^[a-zA-Z0-9]*$', max_length=50)
    last_name = serializers.RegexField(regex=r'^[a-zA-Z0-9]*$', max_length=50)
    email = serializers.CharField(max_length=25)
    description = serializers.CharField(max_length=255)
    photo_url = serializers.CharField(max_length=255, required=False, allow_null=True)
    address = serializers.CharField(max_length=255)   
    coords = PointField(required=False)
    
    
    class Meta:
        model = User
        geo_field = "coords"
        fields = [
            "username", "password", "first_name", "last_name", "email", "hood", "description", "photo_url", "address", "coords"
        ]
    
    def to_representation(self, instance):
        """
        Gets the coordinates from the address
        """
        hood, coords  = self.process_coords(instance.get("address"))

        instance['hood'] = hood
        instance['coords'] = coords

        return instance

        
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField( max_length=50)
    password = serializers.CharField( max_length=30)
    
class EditUserSerializer(UserSerializer):
    username = serializers.CharField(max_length=50, required=False)
    password = serializers.CharField(max_length=30, required=False)
    first_name = serializers.RegexField(regex=r'^[a-zA-Z0-9]*$', max_length=50, required=False)
    last_name = serializers.RegexField(regex=r'^[a-zA-Z0-9]*$', max_length=50,required=False)
    email = serializers.CharField(max_length=25,required=False)
    description = serializers.CharField(required=False)
    photo_url = serializers.CharField(max_length=255, required=False, allow_null=True)
    address = serializers.CharField(max_length=200, required=False)   
    
    def to_representation(self, instance):
        """
        Gets the coordinates from the address
        """
        if instance.get("coords"):
            hood_id = self.process_coords()
            instance['coords'] = f"({self.coords[0]} {self.coords[1]})"
            instance['hood_id'] = hood_id
            instance['location_confirmed'] = self.confirm_hood(hood_id)

        return instance