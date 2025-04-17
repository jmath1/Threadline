from celery import shared_task
from django.conf import settings
import redis
import uuid
import json
import Notification from main.models

redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

@shared_task
def create_notification(user_id, notification_type, related_model, related_model_id):
    """
    add notification to pubsub for user and to mongo
    """
    internal_id = str(uuid.uuid4())
    notification_data = {
        'id': internal_id,
        'user_id': user_id,
        'type': notification_type,
        'related_model': related_model,
        'related_model_id': related_model_id,
    }
    redis_client.publish(f"notifications:{user_id}", json.dumps(notification_data))
    # Save to MongoDB
    notification = Notification(
        internal_id=internal_id,
        user_id=user_id,
        type=notification_type,
        related_model=related_model,
        related_model_id=related_model_id,
    )
    notification.save()
    