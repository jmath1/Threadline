from django.db.models import Q
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from main.models import Message, Thread
from main.permissions import ThreadPermission
from main.serializers.general import EmptySerializer
from main.serializers.thread import CreateThreadSerializer, ThreadSerializer
from rest_framework import status
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     GenericAPIView, ListAPIView,
                                     RetrieveAPIView, RetrieveDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class GetHoodThreads(ListAPIView):
    permission_classes = [IsAuthenticated, ThreadPermission]
    serializer_class = ThreadSerializer
    
    def get_queryset(self):
        return Thread.objects.filter(hood=self.request.user.hood)
class RetrieveDestroyThread(RetrieveAPIView):
    
    serializer_class = ThreadSerializer
    permission_classes = [IsAuthenticated, ThreadPermission]
    
    def get_queryset(self):
        return Thread.objects.all()

    @swagger_auto_schema(
        operation_description="Get a thread",
        responses={200: ThreadSerializer},
    )
    def get(self, request, pk):
        thread = self.get_object()
        serializer = self.get_serializer(thread)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Delete a thread",
        responses={204: "No Content"},
    )
    def delete(self, request, *args, **kwargs):
        thread = self.get_object()
        thread.delete()
        return Response(status=204)
    
class CreateThread(CreateAPIView):
    serializer_class = CreateThreadSerializer
    permission_classes = [IsAuthenticated]
    queryset = Thread.objects.all()
    
    @swagger_auto_schema(
        operation_description="Create a thread",
        responses={201: ThreadSerializer},
    )
    def post(self, request):
        """
        Create a thread, create message, associate message and partipants
        """
        data = request.data.dict()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        thread = serializer.save()
        return Response(serializer.data, status=201)



# Follow a thread
class FollowThread(GenericAPIView):
    serializer_class = EmptySerializer

    @swagger_auto_schema(
        operation_description="Follow a thread",
        responses={200: "Thread followed successfully.", 400: "Already following this thread."}
    )
    def post(self, request, thread_id):
        thread = get_object_or_404(Thread, id=thread_id)
        if request.user in thread.followers.all():
            return Response({"detail": "Already following this thread."}, status=status.HTTP_400_BAD_REQUEST)
        thread.followers.add(request.user)
        return Response({"detail": "Thread followed successfully."}, status=status.HTTP_200_OK)


class UnfollowThread(GenericAPIView):
    serializer_class = EmptySerializer

    @swagger_auto_schema(
        operation_description="Unfollow a thread",
        responses={200: "Thread unfollowed successfully.", 400: "You are not following this thread."}
    )
    def post(self, request, thread_id):
        thread = get_object_or_404(Thread, id=thread_id)
        if request.user not in thread.followers.all():
            return Response({"detail": "You are not following this thread."}, status=status.HTTP_400_BAD_REQUEST)
        thread.followers.remove(request.user)
        return Response({"detail": "Thread unfollowed successfully."}, status=status.HTTP_200_OK)


class GetRecentlyCreatedThreads(ListAPIView):
    serializer_class = ThreadSerializer

    @swagger_auto_schema(
        operation_description="Get recently created threads",
        responses={200: ThreadSerializer(many=True)},
    )
    def get_queryset(self):
        return Thread.objects.filter(
            Q(type="PUBLIC") | \
                Q(hood=self.request.user.hood) | \
                    Q(participants=self.request.user)) \
                        .order_by("-created_at")
                        
class GetThreadsWithNewMessages(ListAPIView):
    serializer_class = ThreadSerializer

    @swagger_auto_schema(
        operation_description="Get threads with new messages",
        responses={200: ThreadSerializer(many=True)},
    )
    def get_queryset(self):
        threads = Thread.objects.filter(
            Q(type="PUBLIC") | 
            Q(hood=self.request.user.hood) | 
            Q(participants=self.request.user)
        )
        threads_with_newest_messages = lambda t: Message.objects.filter(thread_id=t.id).order_by('-created_at').first().created_at
        threads = sorted(threads, key=threads_with_newest_messages, reverse=True)
        return threads
