from django.contrib.auth.hashers import check_password, make_password
from django.http import JsonResponse
from main.api.general import CustomAPIView
from main.auth import JWTAuthentication, LoginRequiredPermission
from main.serializers import (EditProfileSerializer, FriendshipSerializer,
                              LoginSerializer, ProfileSerializer)
from main.utils.utils import (execute, get_user_id, query_to_json, run_query,
                              sanitize_json_input)
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.response import Response
from rest_framework.views import APIView


class AddFriendView(CustomAPIView):
    permission_classes = [LoginRequiredPermission]

    def post(self, request):
        user_id = get_user_id(request)
        if not request.data.get('user_id'):
            return Response({"error": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        sql_query = "SELECT * FROM Friendship \
            WHERE confirmed = TRUE AND (follower_id = {} AND followee_id = {}) \
            OR (followee_id = {} AND follower_id = {})".format(
                user_id, request.data['user_id'], user_id, request.data['user_id'])
            
        if run_query(sql_query):
            return Response({"error": "User already a friend"}, status=400)
        
        execute(
            "INSERT INTO Friendship (follower_id, followee_id, requested, confirmed) VALUES (%s, %s, TRUE, FALSE)".format(
            [user_id, request.data['user_id']])
        )
        return Response({"status": "Friendship request sent"}, status=status.HTTP_201_CREATED)

class DeleteFollowerView(CustomAPIView):
    permission_classes = [LoginRequiredPermission]
    def post(self, request):
        user_id = get_user_id(request)
        follower_id = request.data.get('user_id')
        if not follower_id:
            return Response({"error": "user_id to delete is required"}, status=status.HTTP_400_BAD_REQUEST)
        row_exists = query_to_json(f"SELECT * FROM Friendship WHERE follower_id = {follower_id} AND followee_id = {user_id} AND requested = FALSE")
        if row_exists:
            execute(f"DELETE FROM Friendship WHERE follower_id = {follower_id} AND followee_id = {user_id} AND requested = FALSE")
            return Response({"status": "Follower deleted"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "User is not a follower"}, status=status.HTTP_400_BAD_REQUEST)
    
    
class DeleteFriendView(CustomAPIView):
    permission_classes = [LoginRequiredPermission]

    def post(self, request):
        user_id = get_user_id(request)
        pk = request.data.get('user_id')
        
        friendship = query_to_json(
            f"SELECT follower_id, followee_id FROM Friendship \
                WHERE (follower_id = {user_id} OR followee_id = {pk}) \
                OR (followee_id = {user_id} OR follower_id = {pk}) \
                AND confirmed = TRUE"
        )
        if not friendship:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if friendship[0]['follower_id'] == user_id:
            execute(
                f"DELETE FROM Friendship WHERE follower_id = {user_id} OR followee_id = {pk}"
            )
        elif friendship[0]['followee_id'] == user_id:
            execute(
                f"UPDATE Friendship SET confirmed = FALSE, requestd = FALSE WHERE follower_id = {pk} OR followee_id = {user_id}"
            )
        return Response({"status": "Friendship updated"}, status=status.HTTP_204_NO_CONTENT)
    
class UnfollowView(CustomAPIView):
    permission_classes = [LoginRequiredPermission]

    def post(self, request, pk):
        followee_id = request.data.get('user_id')
        user_id = get_user_id(request)
        if not followee_id:
            return Response({"error": "user_id to unfollow is required"}, status=status.HTTP_400_BAD_REQUEST)
        row_exists = query_to_json("SELECT * FROM Friendship WHERE follower_id = %s AND followee_id = %s", [user_id, followee_id])
        if row_exists:
            execute("DELETE FROM Friendship WHERE follower_id = %s", [pk])
            return Response({"status": "Unfollowed"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "not found"}, status=status.HTTP_404_NOT_FOUND)
        
class FollowView(CustomAPIView):
    permission_classes = [LoginRequiredPermission]

    def post(self, request):
        # gets the user_id of the user making the request
        user_id = get_user_id(request)
        followee_id = request.data.get('user_id')
        if not followee_id:
            return Response({"error": "user_id to follow is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # check existing friendship
        sql_query = "SELECT * FROM Friendship WHERE follower_id = %s AND followee_id = %s"
        existing_friendship = execute(sql_query,params=[user_id, followee_id], fetch=True)
        if existing_friendship:
            return Response({"status": "Already following"}, status=status.HTTP_400_BAD_REQUEST)
        # initiate a new friendship. note that confirmed and requested are set to false,
        # indicating that it is just a follow and not a confirmed or pending "friendship"
        execute(
            "INSERT INTO Friendship (follower_id, followee_id, requested, confirmed) VALUES ({}, {}, FALSE, FALSE)",
            params=(user_id, followee_id))
        return Response({"status": "Follow request sent"}, status=status.HTTP_201_CREATED)

class AcceptFriendshipView(CustomAPIView):
    permission_classes = [LoginRequiredPermission]

    def post(self, request):
        user_id = get_user_id(request)
        follower_id = request.data.get('user_id')
        if not follower_id:
            return Response({"error": "user_id to accept friendship is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        execute("UPDATE Friendship SET confirmed = TRUE, requested = FALSE WHERE follower_id = {} AND followee_id = {}".format(
            follower_id, user_id
        ))

        return Response({"status": "Friendship accepted"}, status=status.HTTP_200_OK)

class DeclineFriendshipView(CustomAPIView):
    permission_classes = [LoginRequiredPermission]

    def post(self, request):
        user_id = get_user_id(request)
        follower_id = request.data.get('user_id')
        if not follower_id:
            return Response({"error": "user_id to decline friendship is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        execute("UPDATE Friendship SET confirmed = FALSE, requested = FALSE WHERE follower_id = {} AND followee_id = {}".format(follower_id, user_id))
     
        return Response(status=status.HTTP_204_NO_CONTENT)

class FriendshipRequestsView(CustomAPIView):
    permission_classes = [LoginRequiredPermission]

    def get(self, request):
        user_id = get_user_id(request)
        result = query_to_json("SELECT p.user_id, p.username, p.first_name, p.last_name FROM Friendship f JOIN Profile p ON p.user_id=f.follower_id  WHERE f.followee_id = {} AND requested = TRUE AND confirmed = FALSE".format(user_id))
        return Response(result)
    
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
            SELECT p.username, p.user_id, p.first_name, p.last_name, b.name AS block_name, h.name as hood_name
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
            
            return Response(serializer.data, status=status.HTTP_201_threadD)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetNeighborList(CustomAPIView):
    permission_classes = [LoginRequiredPermission]
    
    def get(self, request):
        user = self.get_user()
        user_id = user['user_id']
        block_id = user['block_id']
        hood_id = user['hood_id']


        block_params = (block_id, user_id)
        block_neighbors_query = "SELECT p.user_id, p.username, p.first_name, p.last_name \
                FROM Profile p JOIN Block b ON b.block_id = p.block_id WHERE b.block_id = %s AND p.user_id != %s;".format(block_id, user_id)

        hood_params = (hood_id, user_id)
        hood_neighbors_query = 'SELECT p.user_id, p.username, p.first_name, p.last_name \
            FROM Profile p \
            JOIN Block b ON b.block_id = p.block_id \
            WHERE b.hood_id = %s AND p.user_id != %s;'.format(hood_params)
            
        
        friendships_params = (user_id, user_id, user_id, user_id)
        friendships_query = """
            SELECT CASE
                       WHEN follower_id = %s THEN followee_id
                       WHEN followee_id = %s THEN follower_id
                   END AS user_id
            FROM Friendship
            WHERE (follower_id = %s OR followee_id = %s) AND confirmed = TRUE;
        """.format(friendships_params)
        

        following_params = (user_id,)
        following_query = """
            SELECT followee_id AS user_id
            FROM Friendship
            WHERE follower_id = %s AND confirmed = FALSE;
        """.format(following_params)

        
        friendships = query_to_json(friendships_query, params=friendships_params)
        following = query_to_json(following_query, params=following_params)
        block_neighbors = query_to_json(block_neighbors_query, params=block_params)
        hood_neighbors = query_to_json(hood_neighbors_query, params=hood_params)
        
        results = {
            "block_neighbors": block_neighbors,
            "hood_neighbors": hood_neighbors,
            "friendships_list": friendships,
            "following_list": following
        }

        return JsonResponse(results)


