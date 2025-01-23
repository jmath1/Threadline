from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from main.serializers.friendship import FriendshipRequestSerializer
from main.models import User, Friendship
from rest_framework.generics import GenericAPIView, ListAPIView, ListCreateAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from django.shortcuts import get_object_or_404

class ListFriendshipView(ListAPIView):
    
    serializer_class = FriendshipRequestSerializer
    
    def get_queryset(self):
        return self.request.user.get_friends()

class ListCreateFriendRequestsView(ListCreateAPIView):
    
    serializer_class = FriendshipRequestSerializer
   
    def get_queryset(self):
        return self.request.user.get_friend_requests()
    
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

    def get_queryset(self):
        return Friendship.objects.filter(to_user=self.request.user, status='REQUESTED')

    def post(self, request, *args, **kwargs):
        friend_request = self.get_object()
        friend_request.accept()
        return Response(status=status.HTTP_200_OK)

class RejectFriendRequestView(GenericAPIView):
    
    def get_queryset(self):
        return Friendship.objects.filter(to_user=self.request.user, status='REQUESTED')
    
    def post(self, request, *args, **kwargs):
        friend_request = self.get_object()
        friend_request.reject()
        return Response(status=status.HTTP_200_OK)

class RemoveFriendView(DestroyAPIView):
    
    def get_queryset(self):
        return Friendship.objects.filter(from_user=self.request.user, status__in=["ACCEPTED", "PENDING"])
    
    def perform_destroy(self, instance):
        instance.delete()