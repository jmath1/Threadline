from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from main.models import User
from main.serializers.follow import FollowerUserSerializer
from main.serializers.general import EmptySerializer
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class FollowViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == "list_followers" or self.action == "list_following":
            return FollowerUserSerializer
        return EmptySerializer

    
    @swagger_auto_schema(
        operation_description="List all followers of the authenticated user",
        responses={200: FollowerUserSerializer(many=True)},
    )
    def list_followers(self, request):
        followers = request.user.get_followers()
        serializer = FollowerUserSerializer(followers, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="List all users the authenticated user is following",
        responses={200: FollowerUserSerializer(many=True)},
    )
    def list_following(self, request):
        following = request.user.get_following()
        serializer = FollowerUserSerializer(following, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Follow a user",
        responses={201: "Started following."},
    )
    def follow(self, request, followee_id):
        if not followee_id:
            return Response({"error": "followee_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        followee = User.objects.get(id=followee_id)
        request.user.follow(followee)
        return Response({"message": "Started following."}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Unfollow a user",
        responses={204: "No Content"},
    )
    def unfollow(self, request, followee_id):
        followee = get_object_or_404(User, id=followee_id)
        request.user.unfollow(followee)
        return Response({"message": "Unfollowed."}, status=status.HTTP_204_NO_CONTENT)
