from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from main.models import User
from main.serializers.follow import FollowSerializer, FollowerSerializer

class FollowViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer

    def list_followers(self, request):
        """List all followers of the authenticated user."""
        followers = request.user.get_followers()
        serializer = FollowerSerializer(followers, many=True)
        return Response(serializer.data)

    def list_following(self, request):
        """List all users the authenticated user is following."""
        following = request.user.get_following()
        serializer = FollowerSerializer(following, many=True)
        return Response(serializer.data)

    def follow(self, request, followee_id):
        """Follow a user."""
        if not followee_id:
            return Response({"error": "followee_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        followee = User.objects.get(id=followee_id)
        request.user.follow(followee)
        return Response({"message": "Started following."}, status=status.HTTP_201_CREATED)

    def unfollow(self, request, followee_id):
        """Unfollow a user."""
        followee = get_object_or_404(User, id=followee_id)
        request.user.unfollow(followee)
        return Response({"message": "Unfollowed."}, status=status.HTTP_204_NO_CONTENT)
