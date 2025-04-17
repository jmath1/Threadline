# Create your models here.
import json
import logging
import re
import uuid
from datetime import datetime

import redis
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        UserManager)
from django.contrib.gis.db import models as gis_models
from django.db import models
from django.utils.functional import cached_property
from main.constants import (FRIEND_REQUEST_STATUS_CHOICES,
                            NOTIFICATION_STATUSES, NOTIFICATION_TYPES,
                            THREAD_TYPES)
from main.utils.utils import decode_external_id, encode_internal_id
from mongoengine import (DateTimeField, Document, EmbeddedDocument,
                         EmbeddedDocumentField, IntField, ListField,
                         StringField)
from mongoengine.queryset import QuerySet

logger = logging.getLogger(__name__)

redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

class Hood(models.Model):
    name = models.CharField(max_length=50, unique=True)
    polygon = gis_models.MultiPolygonField(srid=4326)

    def __str__(self):
        return self.name

    def get_member_count(self):
        return self.user_set.count()
    
    @property
    def member_count(self):
        return self.get_member_count()
    
    @property
    def members(self):
        return self.user_set.all()

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    description = models.TextField()
    photo_url = models.CharField(max_length=255, null=True)
    coords = gis_models.PointField(geography=True, srid=4326)
    location_confirmed = models.BooleanField(default=False)
    address = models.CharField(max_length=255)
    hood = models.ForeignKey(Hood, on_delete=models.SET_NULL, null=True)
    hood_follow = models.ManyToManyField(Hood, through='UserFollowHood', related_name='hood_follow')
    friends = models.ManyToManyField('self', through='Friendship', symmetrical=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'password', 'first_name', 'last_name']
    is_anonymous = False
    
    objects = UserManager()

    @cached_property
    def friends_count(self):
        return self.friends.count()

    @cached_property
    def followers_count(self):
        return self.get_followers().count()
    
    @cached_property
    def following_count(self):
        return self.get_following().count()
    
    
    def get_user_hood_and_block(self) -> int:
        
        hood_id = User.objects.get(user_id=self.user_id).only("hood_id")

        return hood_id

    def __str__(self):
        return f"User {self.pk} {self.username}"

    def confirm_location(self, hood) -> bool:
        confirmed = False
        if hood.get_member_count() <= 3:
            confirmed = True
        else:
            # count user block approvals for block_id and user_id
            if UserHoodApproval.objects.count(hood.id, self.user_id) >= 3:
                confirmed = True
        
        if confirmed != self.location_confirmed:
            self.location_confirmed = confirmed
            self.save()
            
        return confirmed


    def send_friend_request(self, to_user):
        Friendship.objects.create(from_user=self, to_user=to_user, status="REQUESTED")

    def accept_friend_request(self, from_user):
        friendship = Friendship.objects.get(from_user=from_user, to_user=self, status="REQUESTED")
        friendship.status = "ACCEPTED"
        friendship.save()

    def remove_friend(self, friend):
        Friendship.objects.filter(
            models.Q(from_user=self, to_user=friend) |
            models.Q(from_user=friend, to_user=self),
            status="ACCEPTED"
        ).delete()

    def follow(self, user):
        Follow.objects.get_or_create(follower=self, followee=user)

    def unfollow(self, user):
        Follow.objects.filter(follower=self, followee=user).delete()

    @cached_property
    def friends(self):
        return User.objects.filter(
            models.Q(friend_requests_sent__to_user=self, friend_requests_sent__status="ACCEPTED") |
            models.Q(friend_requests_received__from_user=self, friend_requests_received__status="ACCEPTED")
        )
        
    def get_friend_requests(self):
        return Friendship.objects.filter(to_user=self, status="REQUESTED")

    def get_followers(self):
        return User.objects.filter(following__followee=self)

    def get_following(self):
        return User.objects.filter(followers__follower=self)
    
    def get_hoods_followed(self):
        return self.hood_follow.all()


class UserHoodApproval(models.Model):
    hood_id = models.ForeignKey(Hood, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    approver_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approver')

    class Meta:
        unique_together = (('hood_id', 'user_id', 'approver_id'),)
        
    def __str__(self):
        return f"{self.approver_id.username} approved {self.user_id.username} for {self.hood_id.name}"


class UserFollowHood(models.Model):
    hood = models.ForeignKey(Hood, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = (('hood_id', 'user_id'),)
        
    def __str__(self):
        return f"{self.user.username} follows {self.hood.name}"


class Friendship(models.Model):

    from_user = models.ForeignKey(User, related_name='friend_requests_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='friend_requests_received', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=FRIEND_REQUEST_STATUS_CHOICES, default='REQUESTED')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('from_user', 'to_user')
        indexes = [
            models.Index(fields=['from_user', 'to_user']),
            models.Index(fields=['status']),
        ]
        
    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username} ({self.status})"

    def accept(self):
        self.status = "ACCEPTED"
        self.save()
    
    def reject(self):
        self.status = "REJECTED"
        self.save()
        
class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followee = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followee')
        indexes = [
            models.Index(fields=['follower', 'followee']),
        ]
        
    def __str__(self):
        return f"{self.follower.username} -> {self.followee.username}"

class Thread(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=10, choices=THREAD_TYPES)
    hood = models.ForeignKey(
        Hood,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='threads'
    )
    participants = models.ManyToManyField(
        User,
        related_name='threads',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_threads'
    )

    @cached_property
    def messages(self):
        # Return all messages in the thread (from mongo)
        return Message.objects(thread_id=self.id)
    
    def __str__(self):
        return self.name if self.name else f"{self.type} thread"
    
    @cached_property
    def participant_users(self):
        return self.participants.all()

class MessageQueryset(QuerySet):
    def get(self, *args, **kwargs):
        if not kwargs.get('external_id'):
            raise ValueError("external_id is required")
        external_id = kwargs.pop('external_id')
        message_id = decode_external_id(external_id)
        return super().get(*args, **kwargs, id=message_id)

class Tag(EmbeddedDocument):
    user_id = IntField(required=True)
    username = StringField(required=True)
    
    def __str__(self):
        return f"Tag {self.username}"
    
class Message(Document):
    thread_id = IntField(required=True)  # Reference to Thread in PostgreSQL
    author_id = IntField(required=True)  # Reference to User in PostgreSQL
    content = StringField(required=True, max_length=1000)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    # the tagged users ids and usernames
    tags = ListField(EmbeddedDocumentField(Tag), required=False)  # the tagged users ids and usernames

    meta = {
        'collection': 'messages',
        'indexes': ['thread_id', 'author_id', 'tags'],
        'queryset_class': MessageQueryset,
    }
    
    @cached_property
    def author(self):
        return User.objects.get(id=self.author_id)
    
    @cached_property
    def external_id(self):
        return encode_internal_id(self.id)

    @cached_property
    def thread(self):
        return Thread.objects.get(id=self.thread_id)
    
    def get_participants_and_tagged_users_to_notify(self):
        mentioned_users = set(re.findall(r'@(\w+)', self.content))
        # if there is a hood, the user can tag hood members
        if self.thread.hood:
            available_users = self.thread.hood.members
        else:
            # user can tag friends
            available_users = self.author.friends | self.thread.participant_users
        tagged_users = available_users.filter(username__in=[x[0:] for x in mentioned_users])
        participants_to_notify = self.thread.participant_users.exclude(id__in=[x.id for x in tagged_users]).exclude(id=self.author_id)
        # add tagged users to the participants but dont send them notifications, they'll receive other notifications
        return participants_to_notify, tagged_users
    
    def build_notification_data(self, users, notification_type):
        return [
            {
                "thread_id": self.thread_id,
                "message_id": self.external_id,
                "author_username": self.author.username,
                "type": notification_type,
                "user_to_notify": user.id,
                "id": str(uuid.uuid4())
            } for user in users
        ]
    
    def notify_users(self, participants_to_notify, tagged_users):
        new_message_notification_data = self.build_notification_data(participants_to_notify, "NEW MESSAGE")
        tagged_users_notification_data = self.build_notification_data(tagged_users, "TAGGED")
        notification_data = new_message_notification_data + tagged_users_notification_data
        for notification in notification_data:
            user = notification['user_to_notify']
            del notification['user_to_notify']
            redis_key = f"notifications:user:{user}"
            redis_client.lpush(redis_key, json.dumps(notification))
            redis_client.ltrim(redis_key, 0, 99)

    def create_tags(self, tagged_users):
        tags = []
        for user in tagged_users:
            tags.append(Tag(user_id=user.id, username=user.username))
        self.tags = tags
            
    def save(self, *args, **kwargs):
        if self.author not in self.thread.participants.all():
            self.thread.participants.add(self.author)
            
        thread = Thread.objects.get(id=self.thread_id)
        partipants_to_notify, newly_tagged_users = self.get_participants_and_tagged_users_to_notify()
        self.create_tags(newly_tagged_users)
        instance = super().save(*args, **kwargs)
        self.notify_users(partipants_to_notify, newly_tagged_users)
    
        thread.participants.add(*newly_tagged_users)
        
        return instance
    
    def __str__(self):
        return f"Message {self.external_id} in thread {self.thread_id} by {self.author_id}"

class UserAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=models.functions.Now())
    
    def __str__(self):
        return f"User {self.user.username} accessed thread {self.thread.name}"

class Notification(Document):
    internal_id = StringField(required=True, default=lambda: str(uuid.uuid4()))
    user_id = IntField(required=True)
    type = StringField(choices=NOTIFICATION_TYPES, required=True)
    related_model = StringField(choices=["thread", "message"], required=True)
    related_model_id = IntField(required=True)
    status = StringField(choices=NOTIFICATION_STATUSES, default="UNREAD")
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'notifications',
        'indexes': ['user_id', 'type', 'related_model', 'related_model_id'],
    }
    
    def __str__(self):
        return f"Notification {self.id} for user {self.user_id}"