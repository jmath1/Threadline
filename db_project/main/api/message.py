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
from rest_framework.exceptions import NotFound

# Edit a message
class UpdateDestroyMessage(RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    permission_classes = [MessagePermission, IsAuthenticated]
    
    def get_object(self):
        """
        Ensures that we retrieve the object safely and handle errors before permissions.
        """
        external_id = self.kwargs.get('external_id')
        try:
            message = Message.objects.get(external_id=external_id)
            return message
        except Message.DoesNotExist:
            raise NotFound("Message not found")

    def get_queryset(self):
        return Message.objects.filter(author_id=self.request.user.id)

    @swagger_auto_schema(
        operation_description="Edit a message",
        request_body=MessageSerializer,
        responses={200: MessageSerializer, 404: "Message not found."}
    )
    def put(self, request, *args, **kwargs):
        message = self.get_object()
        if message.author_id != request.user.id:
            return Response({"detail": "You do not have permission to edit this message."}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(message, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(
        operation_description="Delete a message",
        responses={200: "Message deleted successfully.", 404: "Message not found."}
    )
    def delete(self, request, *args, **kwargs):
        message = self.get_object()
        if message.author_id != request.user.id:
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
        data = self.request.data.dict()
        author_id = self.request.user.id
        data['author_id'] = author_id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)