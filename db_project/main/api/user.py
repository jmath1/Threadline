from django.contrib.auth.hashers import check_password, make_password
from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from main.api.general import CustomAPIView
from main.auth import JWTAuthentication, LoginRequiredPermission
from main.serializers import (EditProfileSerializer, LoginSerializer,
                              ProfileSerializer)
from main.utils.utils import (execute, get_user_id, query_to_json, run_query,
                              sanitize_json_input)


class GetUserDetail(APIView):
    permission_classes = [LoginRequiredPermission]
    
    def get(self, request, user_id):
        sql_query = f"""
            SELECT p.username, p.first_name, p.last_name, p.email, b.name AS block_name, h.name as hood_name
            FROM Profile p
            JOIN Block b ON p.block_id = b.block_id
            JOIN Hood h ON b.hood_id = h.hood_id
            WHERE p.user_id = {user_id};
        """
        data = query_to_json(sql_query)
        followers_count = run_query(f"SELECT COUNT(*) FROM Friendship WHERE followee_id = {user_id} AND confirmed=false;")[0]["count"]
        following_count = run_query(f"SELECT COUNT(*) FROM Friendship WHERE follower_id = {user_id} AND confirmed=false;")[0]["count"]
        friends_count = run_query(f"SELECT COUNT(*) FROM Friendship WHERE (follower_id = {user_id} OR followee_id = {user_id}) AND confirmed=true;")[0]["count"]
        data[0]["followers_count"] = followers_count
        data[0]["following_count"] = following_count
        data[0]["friends_count"] = friends_count
        
        if data:
            return JsonResponse({"results": data})
        return JsonResponse({}, status=404)
    
class GetFollowers(CustomAPIView):
    permission_classes = [LoginRequiredPermission]
    
    def get(self, request):
        user_id = self.get_user()["user_id"]
        sql_query = f"""
            SELECT p.username, p.first_name, p.last_name, b.name AS block_name, h.name as hood_name
            FROM Profile p
            JOIN Block b ON p.block_id = b.block_id
            JOIN Hood h ON b.hood_id = h.hood_id
            JOIN Friendship f ON p.user_id = f.follower_id
            WHERE f.followee_id = {user_id} AND f.confirmed=false;
        """
        data = query_to_json(sql_query)
        if data:
            return JsonResponse({"results": data})
        return JsonResponse({"results": []})
    
class GetFollowing(CustomAPIView):
    def get(self, request):
        user_id = self.get_user()["user_id"]
        sql_query = f"""
            SELECT p.username, p.user_id, p.first_name, p.last_name, b.name AS block_name, h.name as hood_name
            FROM Profile p
            JOIN Block b ON p.block_id = b.block_id
            JOIN Hood h ON b.hood_id = h.hood_id
            JOIN Friendship f ON p.user_id = f.followee_id
            WHERE f.follower_id = {user_id} AND f.confirmed=false;
        """
        data = query_to_json(sql_query)
        if data:
            return JsonResponse({"results": data})
        return JsonResponse({"results": []})

class GetFriendsList(CustomAPIView):
    permission_classes = [LoginRequiredPermission]
    
    def get(self, request):
        user_id = self.get_user()["user_id"]
        sql_query = f"""
            SELECT p.username, p.user_id, p.first_name, p.last_name, b.name AS block_name, h.name as hood_name
            FROM Profile p
            JOIN Block b ON p.block_id = b.block_id
            JOIN Hood h ON b.hood_id = h.hood_id
            JOIN Friendship f ON p.user_id = f.followee_id
            WHERE f.follower_id = {user_id} AND f.confirmed=true
            UNION
            SELECT p.username, p.user_id, p.first_name, p.last_name, b.name AS block_name, h.name as hood_name
            FROM Profile p
            JOIN Block b ON p.block_id = b.block_id
            JOIN Hood h ON b.hood_id = h.hood_id
            JOIN Friendship f ON p.user_id = f.follower_id
            WHERE f.followee_id = {user_id} AND f.confirmed=true;
        """
        data = query_to_json(sql_query)
        if data:
            return JsonResponse({"results": data})
        return JsonResponse({"results": []})

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
            user_id = result[0]["user_id"]
            return user_id
        else:
            return None

    def post(self, request):
        data = sanitize_json_input(request.data)
        serializer = ProfileSerializer(data=data)
        if serializer.is_valid():
            user_id = self.save(**serializer.data)
            token = JWTAuthentication().refresh_token(user_id)
            response = Response(status=status.HTTP_201_CREATED, data = {"user_id": user_id, "jwt_token": token})
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileLogin(APIView):    

    def post(self, request):
        data = sanitize_json_input(request.data)
        serializer = LoginSerializer(data=data)
        username = None
        if serializer.is_valid():
            username = serializer.data['username']
            hashed_password_input = serializer.data['password']
        if not username or not hashed_password_input:
            raise AuthenticationFailed('Please provide both username and password')
        user_query = run_query("""SELECT password, user_id FROM Profile WHERE username = '{username}';""".format(username=username))

        if user_query:
            hashed_password_from_db = user_query[0]["password"]
            
        if check_password(hashed_password_input, hashed_password_from_db):
            user_id = user_query[0]["user_id"]
            response = Response(status=200, data = {"jwt_token": JWTAuthentication().refresh_token(user_id)})        
            return response
        else:
            raise AuthenticationFailed('Invalid username or password')

class MeGET(CustomAPIView):
    permission_classes = [LoginRequiredPermission]
    
    def get(self, request):
        user = self.get_user()
        sql_query = f"""SELECT p.*, b.hood_id 
                        FROM Profile p 
                        JOIN Block b ON p.block_id = b.block_id 
                        WHERE p.user_id = {get_user_id(request)};"""

        data = run_query(sql_query)[0]
        del data["password"]
        
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
                    if value != 'NULL':
                        set_clauses.append("{field}='{value}'".format(
                            field=field,
                            value=value
                        ))
                    else:
                        set_clauses.append("{field}={value}".format(
                            field=field,
                            value=value
                        ))

        set_clause = ", ".join(set_clauses)

        sql_query = f"""
            UPDATE Profile 
            SET {set_clause}
            WHERE user_id={user_id};
        """
        result = execute(sql_query)

        if result:
            return user_id
        else:
            return None

    def post(self, request):
        data = sanitize_json_input(request.data)
        serializer = EditProfileSerializer(data=data)

        if serializer.is_valid(request=request):
            self.save(request.user, **serializer.data)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Users
class GetNeighborList(CustomAPIView):
    permission_classes = [LoginRequiredPermission]
    def get(self, request):
        user = self.get_user()
       
        block_neighbors  = f"""
            SELECT p.user_id, p.username, p.first_name, p.last_name, p.email
            FROM Profile p WHERE p.block_id={user["block_id"]};
        """
        hood_neighbors = f"""
            SELECT p.user_id, p.username, p.first_name, p.last_name, p.email
            FROM Profile p 
            JOIN Block b ON b.block_id = p.block_id
            WHERE b.hood_id = {user["hood_id"]} AND p.block_id != {user["block_id"]};
        """

        results = {
            "block_neighbors": query_to_json(block_neighbors),
            "hood_neighbors": query_to_json(hood_neighbors)
        }

        return JsonResponse(results)
