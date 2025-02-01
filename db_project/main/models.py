# Create your models here.
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        UserManager)
from django.contrib.gis.db import models as gis_models
from django.db import models
from main.constants import (FRIEND_REQUEST_STATUS_CHOICES,
                            NOTIFICATION_STATUSES, NOTIFICATION_TYPES,
                            THREAD_TYPES)
from mongoengine import Document, StringField, DateTimeField, IntField, ListField, EmbeddedDocument, EmbeddedDocumentField
from datetime import datetime
from main.utils.utils import encode_internal_id, decode_external_id
from mongoengine.queryset import QuerySet

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

    @property
    def is_authenticated(self):
        return True
    
    @property
    def friends_count(self):
        return self.get_friends().count()
    
    @property
    def followers_count(self):
        return self.get_followers().count()
    
    @property
    def following_count(self):
        return self.get_following().count()
    
    
    def get_user_hood_and_block(self) -> int:
        
        hood_id = User.objects.get(user_id=self.user_id).only("hood_id")

        return hood_id

    def __str__(self):
        return f"User {self.pk} self.username"

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

    def get_friends(self):
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

    @property
    def messages(self):
        # Return all messages in the thread (from mongo)
        return Message.objects(thread_id=self.id)
    
    def __str__(self):
        return self.name if self.name else f"{self.type} thread"

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
    
    @property
    def external_id(self):
        return encode_internal_id(self.id)
    
class UserAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=models.functions.Now())
    
    def __str__(self):
        return f"User {self.user.username} accessed thread {self.thread.name}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')    
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, null=True)
    message_id = models.IntegerField()
    friendship = models.ForeignKey(Friendship, on_delete=models.CASCADE, null=True)
    follow = models.ForeignKey(Follow, on_delete=models.CASCADE, null=True)
    datetime = models.DateTimeField(default=models.functions.Now())
    type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    status = models.CharField(max_length=50, choices=NOTIFICATION_STATUSES, default="UNREAD")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['status']),
        ]
        
    def __str__(self):
        return f"Notification for {self.user.username} - {self.type}"
