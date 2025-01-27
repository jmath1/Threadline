from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from main.models import Message, Thread
from main.permissions import MessagePermission
from main.serializers.thread import MessageSerializer
from rest_framework import status
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


# Edit a message
class UpdateDestroyMessage(RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    permission_classes = [MessagePermission, IsAuthenticated]
    
    def get_queryset(self):
        return Message.objects.filter(author=self.request.user)

    @swagger_auto_schema(
        operation_description="Edit a message",
        request_body=MessageSerializer,
        responses={200: MessageSerializer, 404: "Message not found."}
    )
    def put(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


    @swagger_auto_schema(
        operation_description="Delete a message",
        responses={200: "Message deleted successfully.", 404: "Message not found."}
    )
    def delete(self, request, *args, **kwargs):
        message = self.get_object()
        if message.author != request.user:
            return Response({"detail": "You do not have permission to delete this message."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


class CreateMessage(CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [MessagePermission, IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create a new message in a thread",
        request_body=MessageSerializer,
        responses={201: MessageSerializer, 400: "Invalid data.", 403: "Permission denied."}
    )
    def post(self, serializer):
        data = self.request.data
        thread = get_object_or_404(Thread, id=data.get("thread_id"))
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)