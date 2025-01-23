from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from main.models import Notification

from main.serializers.notification import NotificationSerializer

class NotificationListCreateAPIView(ListCreateAPIView):
   
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        return Notification.objects.filter(user_id=self.request.user.id)
    
class NotificationRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        return Notification.objects.filter(user_id=self.request.user.id)


