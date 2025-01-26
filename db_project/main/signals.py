from django.db.models.signals import post_save
from django.dispatch import receiver
from main.models import Follow, Friendship, Notification


@receiver(post_save, sender=Friendship)
def notify_friend_request(sender, instance, created, **kwargs):
    if created and instance.status == "REQUESTED":
        #print(f"Friend request sent from {instance.from_user} to {instance.to_user}")
        Notification.objects.create(
            user=instance.to_user,
            type="FRIEND_REQUESTED",
            friendship=instance
        )
    elif instance.status == "ACCEPTED":
        #print(f"{instance.from_user} and {instance.to_user} are now friends!")
        Notification.objects.create(
            user=instance.from_user,
            type="FRIEND_ACCEPTED",
            friendship=instance
        )

@receiver(post_save, sender=Follow)
def notify_follower(sender, instance, created, **kwargs):
    if created:
        #print(f"{instance.follower} started following {instance.followee}")
        Notification.objects.create(
            user=instance.followee,
            type="FOLLOW",
            follow=instance
        )
