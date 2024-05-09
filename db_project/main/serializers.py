import requests
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from main.utils.utils import run_query, get_user_id


class ProfileSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=30)
    first_name = serializers.RegexField(regex=r'^[a-zA-Z0-9]*$', max_length=50)
    last_name = serializers.RegexField(regex=r'^[a-zA-Z0-9]*$', max_length=50)
    email = serializers.CharField(max_length=25)
    description = serializers.CharField(max_length=255)
    photo_url = serializers.CharField(max_length=255, required=False)
    address = serializers.CharField(max_length=255)   

    def confirm_block(self, block_id):
        if not block_id and block_id != 0:
            return False
        """
        Checks whether the block has 3 or fewer members. If so, the user location is confirmed.
        """
        sql_query = f"""SELECT COUNT(p.user_id) FROM Profile p 
                        JOIN Block b ON p.block_id = b.block_id 
                        WHERE b.block_id = {block_id} 
                        GROUP BY b.block_id"""
        
        data = run_query(sql_query)
        if data[0]["count"] <= 3:
            self.inital_data = True
            return True
        
        self.inital_data = False
        return False
    
    def to_representation(self, instance):
        """
        Gets the coordinates from the address
        """
        block_id, _ = self.process_coords()
        instance['coords'] = f"({self.coords[0]} {self.coords[1]})"
        instance['block_id'] = block_id
        instance['location_confirmed'] = self.confirm_block(block_id)

        return instance

    def is_valid(self, request=None, raise_exception=False):
        """
        validates username and email
        """
        address = self.initial_data.get("address")
        if address:
            self.geocode_address(address)
            block_id, _ = self.process_coords()
            self.confirm_block(block_id)
        username = self.initial_data.get("username")
        email = self.initial_data.get("email")
        sql_query = f"""
            SELECT COUNT(*) FROM Profile WHERE (username='{username}' OR email='{email}' ) AND user_id != {get_user_id(request)};
        """
        if run_query(sql_query)[0]["count"] > 0:
            raise ValidationError("Username or email already in use")
        
        return super().is_valid(raise_exception=raise_exception)
    
    def process_coords(self):
        """
        Checks to make sure address coords are within a supported block and hood. Returns (block_id, hood_id) if they exist
        """
        sql_query = f"""SELECT block_id FROM Block b WHERE ST_DWithin(
            b.coords,
            ST_GeomFromText('POINT({self.coords[0]} {self.coords[1]})', 4326),
            b.radius
        );"""
        data = run_query(sql_query)
        if not data:
            raise ValidationError("Block not supported")
        else:
            return data[0]["block_id"], None
        
        
    def geocode_address(self, address):
        """
        Gets the latitude and longitude of an address
        """

        special_chars = {'"', "'", ";"}
        if any(char in address for char in special_chars):
            raise ValidationError("It looks like you might be trying something malicious")
        params = {
            'locate': address + " New York, NY",
            'json': 1  ,
            'auth': '354222234714769519100x71435'
        }
        data = {
            "auth": "354222234714769519100x71435"
        }
        response = requests.get("https://geocode.xyz", params=params, data=data)

        if response.status_code == 200:
            if response.json().get("error"):
                raise ValidationError("No results found for the provided address.")
            else:
                latitude = response.json()['latt']
                longitude = response.json()['longt']
                self.coords = (longitude, latitude)

        
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField( max_length=50)
    password = serializers.CharField( max_length=30)
    
class EditProfileSerializer(ProfileSerializer):
    username = serializers.CharField(max_length=50, required=False)
    password = serializers.CharField(max_length=30, required=False)
    first_name = serializers.RegexField(regex=r'^[a-zA-Z0-9]*$', max_length=50, required=False)
    last_name = serializers.RegexField(regex=r'^[a-zA-Z0-9]*$', max_length=50,required=False)
    email = serializers.CharField(max_length=25,required=False)
    description = serializers.CharField(required=False)
    photo_url = serializers.CharField(max_length=255, required=False)
    address = serializers.CharField(max_length=200, required=False)   
    
    def to_representation(self, instance):
        """
        Gets the coordinates from the address
        """
        if instance.get("coords"):
            block_id, _ = self.process_coords()
            instance['coords'] = f"({self.coords[0]} {self.coords[1]})"
            instance['block_id'] = block_id
            instance['location_confirmed'] = self.confirm_block(block_id)

        return instance