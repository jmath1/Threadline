import os

import jwt
import requests
from django.conf import settings
from django.db import connection
from rest_framework.exceptions import ValidationError
from rest_framework.request import QueryDict


def sanitize_json_input(querydict):
    sanitized_querydict = QueryDict(mutable=True)
    for key, v in querydict.items():
        if isinstance(v, str):
            sv = v
            sv = v.replace("'", "''")
            sv = v.replace('"', '\\"')
            sv = v.replace('\\', '\\\\')
            sv = v.replace(';', '\\;')
            sanitized_querydict.appendlist(key, sv)
        else:
            sanitized_querydict.appendlist(key, v)
    return sanitized_querydict

def validate_coords(coords, user, validity_type=None):
    # user threads are validated automatically as True. This way, friends can discuss anything,
    # block threads are only valid within their area.
    # hood threads are valid within the area of their corresponding blocks

    if validity_type is None:
        return True

    if validity_type:
        if validity_type == "user":
            return True
        
        if validity_type == "block":
            sql_query = f"""
                SELECT DISTINCT b.block_id
                FROM Block b
                AND ST_DWithin(ST_Point({coords})::geography, b.center::geography, b.radius)
            """
            data = run_query(sql_query)
            if data and data["block_id"] == user["block_id"]:
                return True
            
        if validity_type == "hood":
            sql_query = f"""
                SELECT DISTINCT b.hood_id
                FROM Block b
                AND ST_DWithin(ST_Point({coords})::geography, b.center::geography, b.radius)
            """
            data = run_query(sql_query)
            if data and data["hood_id"] == user["hood_id"]:
                return True
         
    
    return False
        
        
def get_cords_from_address(address):
    """
    Gets the latitude and longitude of an address
    """

    api_key = os.getenv("GOOGLE_API_KEY")
    endpoint = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": api_key
    }

    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        if response.json().get("error"):
            raise ValidationError("No results found for the provided address.")
        else:
            latitude = response.json()['results'][0]['geometry']['location']['lat']
            longitude = response.json()['results'][0]['geometry']['location']['lng']
            

            return (longitude, latitude)
    return (None, None)

def get_user_id(request):
    payload = jwt.decode(request.headers.get("Authorization"), settings.SECRET_KEY, algorithms=['HS256'])
    return payload.get('user_id')

def execute(sql, params=None, fetch=False):
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        if fetch:
            return cursor.fetchall()
        else:
            connection.commit()

def run_query(sql_query, params=None):
    with connection.cursor() as cursor:
        cursor.execute(sql_query, params or [])
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]


def query_to_json(sql_query, params=None):
    """
    Executes an SQL query and returns the results in JSON format.
    
    Args:
        connection_details (dict): Database connection parameters.
        sql_query (str): SQL query to execute.
        params (tuple): Optional parameters for SQL query to prevent SQL injection.

    Returns:
        str: JSON string containing the query results.
    """    
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_query, params)
            columns = [desc[0] for desc in cursor.description]
            data = cursor.fetchall()
            result = [dict(zip(columns, row)) for row in data]
           
            return result
    except Exception as e:
        print(f"An error occurred: {e}")
        return {'error': str(e)}
    finally:
        connection.close()