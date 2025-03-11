from django.db.models import Q
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from main.models import Friendship, User
from main.serializers.friendship import FriendshipRequestSerializer
from main.serializers.general import EmptySerializer
from rest_framework import status, viewsets
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     GenericAPIView, ListAPIView,
                                     ListCreateAPIView, UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class ListFriendshipView(ListAPIView):
    
    serializer_class = FriendshipRequestSerializer
    
    def get_queryset(self):
        return self.request.user.friends
    
    @swagger_auto_schema(
        operation_description="List all friends of the authenticated user",
        responses={200: FriendshipRequestSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ListCreateFriendRequestsView(ListCreateAPIView):
    
    serializer_class = FriendshipRequestSerializer
   
    def get_queryset(self):
        return self.request.user.get_friend_requests()
    
    @swagger_auto_schema(
        operation_description="List all friend requests of the authenticated user",
        responses={200: FriendshipRequestSerializer(many=True)},
    )
    def post(self, request, *args, **kwargs):
        data = {
            "from_user": request.user.id,
            "to_user": request.data.get("to_user"),
            "status": "REQUESTED"
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class AcceptFriendRequestView(GenericAPIView):
    serializer_class = EmptySerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Friendship.objects.filter(to_user=self.request.user, status='REQUESTED')
        else:
            return Friendship.objects.none()
    @swagger_auto_schema(
        operation_description="Accept a friend request",
        responses={200: "Friend request accepted."},
    )
    def post(self, request, *args, **kwargs):
        friend_request = self.get_object()
        friend_request.accept()
        return Response(status=status.HTTP_200_OK)

class RejectFriendRequestView(GenericAPIView):
    serializer_class = EmptySerializer
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Friendship.objects.filter(to_user=self.request.user, status='REQUESTED')
        else:
            return Friendship.objects.none()
    @swagger_auto_schema(
        operation_description="Reject a friend request",
        responses={200: "Friend request rejected."},
    )
    def post(self, request, *args, **kwargs):
        friend_request = self.get_object()
        friend_request.reject()
        return Response(status=status.HTTP_200_OK)

class RemoveFriendView(DestroyAPIView):
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Friendship.objects.filter((Q(from_user=self.request.user) | Q(to_user=self.request.user)) & Q(status__in=["ACCEPTED", "PENDING"]))
        return Friendship.objects.none()
    
    def perform_destroy(self, instance):
        instance.delete()
        
    @swagger_auto_schema(
        operation_description="Remove a friend",
        responses={204: "No Content"},
    )
    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)