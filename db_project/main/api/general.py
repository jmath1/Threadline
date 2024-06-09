from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponse, JsonResponse
from main.auth import JWTAuthentication, LoginRequiredPermission
from main.serializers import (EditProfileSerializer, LoginSerializer,
                              ProfileSerializer)
from main.utils.utils import execute, get_user_id, query_to_json, run_query
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView


class CustomAPIView(APIView):
    def get_user(self):
        query = f"""
            SELECT user_id, b.block_id, b.hood_id
            FROM Profile p
            JOIN Block b ON b.block_id = p.block_id
            WHERE p.user_id = {get_user_id(self.request)};
        """
        return run_query(query)[0]

class CreateFriendshipRequest(APIView):
    
    permission_classes = [LoginRequiredPermission]
    def post(self, request):
        user_id = get_user_id(request)
        sql_query = f"""
            INSERT INTO Friendship (follower_id, followee_id, confirmed)
            VALUES ({user_id}, {request.data["followee_id"]}, false)
            RETURNING;
        """
        execute(sql_query)
        return JsonResponse(status_code=201)
class GetFriendshipRequests(APIView):
    permission_classes = [LoginRequiredPermission]
    def get(self, request):
        user_id = get_user_id(request)
        sql_query = f"""
            SELECT p.user_id, p.username, p.first_name, p.last_name, p.email
            FROM Profile p
            JOIN Friendship f ON p.user_id = f.follower_id
            WHERE f.followee_id = {user_id} AND confirmed=false;
        """
        return JsonResponse({"results": query_to_json(sql_query)})
    
class ConfirmFriendshipRequest(APIView):
    permission_classes = [LoginRequiredPermission]
    def post(self, request):
        user_id = get_user_id(request)
        sql_query = f"""
            UPDATE Friendship
            SET confirmed=true
            WHERE follower_id={request.data["follower_id"]} AND followee_id={user_id};
        """
        execute(sql_query)
        return JsonResponse(status_code=201)


class GetFollowers(APIView):
    permission_classes = [LoginRequiredPermission]
    
    def get(self, request):
        user_id = get_user_id(request)
        sql_query = f"""
            SELECT p.user_id, p.username, p.first_name, p.last_name, p.email
            FROM Profile p
            JOIN Friendship f ON p.user_id = f.follower_id
            WHERE f.followee_id = {user_id} AND confirmed=true;
        """
        return JsonResponse(query_to_json(sql_query))




# Threads


def get_new_hood_threads(request):
    return JsonResponse({"message": "Get new hood threads endpoint"})

def get_new_block_threads(request):
    return JsonResponse({"message": "Get new block threads endpoint"})

def get_new_user_threads(request):
    return JsonResponse({"message": "Get new user threads endpoint"})


# Notifications
def get_notifications(request):
    return JsonResponse({"message": "Get notifications endpoint"})

