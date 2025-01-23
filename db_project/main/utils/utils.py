import os
import requests
from typing import Tuple
from django.contrib.gis.geos import Point
from main.models import Hood
from rest_framework.exceptions import ValidationError
    
def geocode_address(self, address: str) -> Point:
    """
    Gets the latitude and longitude of an address. Returns None if the address is invalid
    """

    api_key = os.getenv("GOOGLE_API_KEY")
    endpoint = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": api_key
    }

    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        if response.json().get("error_message"):
            return None
        else:
            latitude = response.json()['results'][0]['geometry']['bounds']['northeast']['lat']
            longitude = response.json()['results'][0]['geometry']['bounds']['northeast']['lng']
            self.coords = (longitude, latitude)
            point = Point(longitude, latitude, srid=4326)
            return point
        
def process_coords(address: str) -> Tuple[Hood, Point]:
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
