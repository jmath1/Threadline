import os
from typing import Tuple

import requests
from bson import ObjectId
from django.conf import settings
from django.contrib.gis.geos import Point
from hashids import Hashids
from rest_framework.exceptions import ValidationError

hashids = Hashids(salt=settings.SECRET_KEY, min_length=8)


def encode_internal_id(mongo_id):
    """Convert MongoDB ObjectId to an integer and encode it with Hashids"""
    if isinstance(mongo_id, ObjectId):  
        mongo_int = int(str(mongo_id), 16)  # Convert ObjectId to an integer
        return hashids.encode(mongo_int)
    return ""

def decode_external_id(hashed_id):
    """Decode Hashid back to the original ObjectId"""
    decoded_values = hashids.decode(hashed_id)
    if decoded_values:
        return ObjectId(hex(decoded_values[0])[2:])  # Convert back to ObjectId
    return None

def geocode_address(address: str) -> Point:
    """
    Gets the latitude and longitude of an address. Returns None if the address is invalid
    """
    endpoint = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address + " Philadelphia, PA",
        "format": "json",
        "addressdetails": 1,
        "limit": 1
    }
    headers = {
        "User-Agent": "YourAppName/1.0 (your.email@example.com)"  # Replace with your app details
    }
    response = requests.get(endpoint, params=params, headers=headers)

    if response.status_code == 200:
        
        results = response.json()
        if results:
            latitude = float(results[0]['lat'])
            longitude = float(results[0]['lon'])
            point = Point(longitude, latitude, srid=4326)
            return point
    return None
        
def process_coords(address: str):
    from main.models import Hood
    """
    Checks to make sure address coords are within a supported hood. Returns hood if it exists
    """
    coords = geocode_address(address)
    hood = None

    if coords:
        hood = Hood.objects.filter(polygon__contains=coords).first()
    if not hood:
        raise ValidationError("Hood not supported")
    return hood, coords
