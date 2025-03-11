from celery import shared_task


@shared_task
def create_notification(user_id, notification_type, related_model, related_model_id):
    from main.models import Notification
    Notification.objects.create(
        user_id=user_id,
        type=notification_type,
        related_model=related_model_id,
    )
