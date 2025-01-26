from drf_yasg.utils import swagger_auto_schema
from main.models import Notification
from main.serializers.general import EmptySerializer
from main.serializers.notification import NotificationSerializer
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response


class NotificationListAPIView(ListAPIView):
   
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        return Notification.objects.filter(user_id=self.request.user.id)
    
    @swagger_auto_schema(
        operation_description="Get notifications for the user",
        responses={200: NotificationSerializer},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
class MarkNotificationReadAPIView(GenericAPIView):
    serializer_class = EmptySerializer

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user.id, status="UNREAD")
    
    @swagger_auto_schema(
        operation_description="Mark a notification as read",
        responses={200: NotificationSerializer},
    )
    def put(self, request, *args, **kwargs):
        notification = self.get_object()
        notification.status = "READ"
        notification.save()
        return Response(NotificationSerializer(notification).data)
        