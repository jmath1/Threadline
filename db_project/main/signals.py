from django.db.models.signals import post_save
from django.dispatch import receiver
from main.models import Follow, Friendship, Message
from main.tasks import create_notification


@receiver(post_save, sender=Friendship)
def notify_friend_request(sender, instance, created, **kwargs):
    if created and instance.status == "REQUESTED":
        create_notification.delay(
            user_id=instance.to_user.id,
            notification_type="FRIEND_REQUESTED",
            related_model="friendship",
            related_model_id=instance.id
        )
    elif instance.status == "ACCEPTED":
        create_notification.delay(
            user_id=instance.from_user.id,
            notification_type="FRIEND_ACCEPTED",
            related_model="friendship",
            related_model_id=instance.id
        )


@receiver(post_save, sender=Follow)
def notify_follower(sender, instance, created, **kwargs):
    if created:
        create_notification.delay(
            user_id=instance.followee.id,
            notification_type="FOLLOW",
            related_model="follow",
            related_model_id=instance.id
        )

@receiver(post_save, sender=Message)
def notify_participants(sender, instance, created, **kwargs):
    if created:
        for participant in instance.thread.participants.all():
            create_notification.delay(
                user_id=participant.id,
                notification_type="PARTICIPANT THREAD NEW MESSAGE",
                related_model="message",
                related_model_id=instance.id
            )

@receiver(post_save, sender=Message)
def notify_new_tag(sender, instance, created, **kwargs):
    if created:
        for tag in instance.tags.all():
            create_notification.delay(
                user_id=tag.user_id,
                notification_type="TAGGED",
                related_model="message",
                related_model_id=instance.id
            )
