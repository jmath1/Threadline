import re
import time

import jwt
from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from main.auth import JWTAuthentication

from main.auth import LoginRequiredPermission
from main.serializers import (EditProfileSerializer, LoginSerializer,
                              ProfileSerializer)
from main.utils.utils import run_query, execute


def healthcheck(request):
    return HttpResponse("this is a test")

class CustomAPIView(APIView):
    pass

class ProfileRegisterView(CustomAPIView):

    def save(self, username, first_name, last_name, email, password, coords, block_id, address, location_confirmed, description='NULL', photo_url='NULL'):
        sql_query = """
            INSERT INTO Profile (
                username, first_name, last_name, block_id, email, password, address, 
                description, photo_url, coords, location_confirmed
            )
            VALUES ('{username}', '{first_name}', '{last_name}', {block_id}, '{email}', '{password}', '{address}', '{description}', '{photo_url}', 'POINT{coords}', {location_confirmed})
            RETURNING user_id;
        """.format(
            username=username,
            first_name=first_name,
            last_name=last_name,
            block_id=block_id,
            email=email,
            password=make_password(password),
            address=address,
            description=description,
            photo_url=photo_url,
            coords=coords,
            location_confirmed=location_confirmed
        )
        result = run_query(sql_query)
        if result:
            user_id = result[0][0]
            return user_id
        else:
            return None

    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            user_id = self.save(**serializer.data)
            
            response = Response(status=status.HTTP_201_CREATED, data = {"jwt_token": JWTAuthentication().refresh_token(user_id)})
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileLogin(APIView):    

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.data['username']
            hashed_password_input = serializer.data['password']
        if not username or not hashed_password_input:
            raise AuthenticationFailed('Please provide both username and password')
        user_query = run_query("""SELECT password, user_id FROM Profile WHERE username = '{username}';""".format(username=username))
        hashed_password_from_db = ''

        if user_query:
            hashed_password_from_db = user_query[0][0]
            user_id = user_query[0][1]
        passwords_match = check_password(hashed_password_input, hashed_password_from_db)
        if not passwords_match:
            raise AuthenticationFailed('Invalid username or password')

        response = Response()
        response = Response(status=200, data = {"jwt_token": JWTAuthentication().refresh_token(user_id)})
        
        return response
    
class MeGET(APIView):
    permission_classes = [LoginRequiredPermission]
    
    def get(self, request):
        sql_query = f"""SELECT * FROM Profile WHERE user_id = {request.user};"""
        data = run_query(sql_query)[0]
        data = {
            "user_id": data[0],
            "user_name": data[1],
            "first_name": data[2],
            "last_name": data[3],
            "address": data[4],
            "email": data[5],
            "description": data[7],
            "block_id": data[9],
            "coords": data[10],
            "confirmed": data[11],
        }

        return JsonResponse(data, status=200)

class EditProfileView(APIView):
    permission_classes = [LoginRequiredPermission]

    def save(self, user_id, **kwargs):
        parameters = {}
        set_clauses = []

        for field, value in kwargs.items():
            if value is not None:
                # Format geographic data specifically
                if field == "coords":
                    # Assuming the input for 'coords' is like '(x, y)'
                    parameters[field] = f"{value}', 4326)"
                    set_clauses.append(f"{field}=ST_PointFromText('POINT{value}', 4326)")
                else:
                    # Use the field name as a placeholder key
                    placeholder = field
                    parameters[placeholder] = value
                    set_clauses.append(f"{field}=%({placeholder})s")

        set_clause = ", ".join(set_clauses)

        sql_query = f"""
            UPDATE Profile 
            SET {set_clause}
            WHERE user_id=%(user_id)s;
        """
        # Execute the SQL query, passing the 'parameters' dictionary which includes 'user_id'
        parameters['user_id'] = user_id
        result = execute(sql_query, parameters)  # Assuming 'execute' can handle param dicts

        if result:
            return user_id
        else:
            return None

    def post(self, request):
        serializer = EditProfileSerializer(data=request.data)
       
        if serializer.is_valid():
            self.save(request.user, **serializer.data)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
def create_user(request):
    if request.method == "POST":
        pass
    else:
        return HttpResponse(status_code=405)
    
def logout(request):
    # Clear user's session upon logout
    request.session.clear()


# Users
def get_user_neighbors(request):
    sql_query = f"""
        SELECT p.user_id, p.username, p.first_name, p.last_name, p.email
        FROM Profile p
        WHERE p.block_id = %s
    """, [request.user_id]
    
    return JsonResponse(run_query(sql_query)[0])

def get_followers(request):
    
    sql_query = f"""
        SELECT p.user_id, p.username, p.first_name, p.last_name, p.email
        FROM Profile p
        JOIN Friendship f ON p.user_id = f.follower_id
        WHERE f.followee_id = %s AND confirmed=true;
    """, [request.user.block_id]
    return JsonResponse(run_query(sql_query)[0])


# Blocks
def get_block_threads(request, block_id):
    return JsonResponse({"message": f"Get block {block_id} threads endpoint"})

def list_block_members(request, block_id):
    return JsonResponse({"message": f"List block {block_id} members endpoint"})

def get_block_follows(request):
    return JsonResponse({"message": "Get block follows endpoint"})


# Hoods
def get_hood_threads(request, hood_id):
    return JsonResponse({"message": f"Get hood {hood_id} threads endpoint"})

def list_hood_members(request, hood_id):
    return JsonResponse({"message": f"List hood {hood_id} members endpoint"})

def get_hood_follows(request):
    return JsonResponse({"message": "Get hood follows endpoint"})


# Threads
def get_thread(request, thread_id):
    return JsonResponse({"message": f"Get thread {thread_id} endpoint"})

def get_user_threads(request):
    return JsonResponse({"message": "Get user threads endpoint"})

def get_new_hood_threads(request):
    return JsonResponse({"message": "Get new hood threads endpoint"})

def get_new_block_threads(request):
    return JsonResponse({"message": "Get new block threads endpoint"})

def get_new_user_threads(request):
    return JsonResponse({"message": "Get new user threads endpoint"})


# Notifications
def get_notifications(request):
    return JsonResponse({"message": "Get notifications endpoint"})

