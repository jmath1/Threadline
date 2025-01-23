# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.gis.db import models as gis_models
from django.db import models

from main.managers.friendship import FriendshipManager
from django.contrib.auth.models import UserManager
from main.constants import NOTIFICATION_TYPES, FRIEND_REQUEST_STATUS_CHOICES

class Hood(models.Model):
    name = models.CharField(max_length=50, unique=True)
    polygon = gis_models.MultiPolygonField(srid=4326)

    def __str__(self):
        return self.name

    def get_member_count(self):
        return self.user_set.count()
        
# class Block(models.Model):
#     hood = models.ForeignKey(Hood, on_delete=models.CASCADE)
#     description = models.TextField()
#     name = models.CharField(max_length=100, unique=True)
#     polygon = gis_models.MultiPolygonField()
    
#     objects = BlockManager()


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
    #block_id = models.ForeignKey(Block, on_delete=models.SET_NULL, null=True)
    hood = models.ForeignKey(Hood, on_delete=models.SET_NULL, null=True)
    #block_follow = models.ManyToManyField(Block, through='UserFollowBlock', related_name='block_follow')
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


class UserHoodApproval(models.Model):
    hood_id = models.ForeignKey(Hood, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    approver_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='approver')

    class Meta:
        unique_together = (('hood_id', 'user_id', 'approver_id'),)

# class UserFollowBlock(models.Model):
#     block = models.ForeignKey(Block, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
    
#     class Meta:
#         unique_together = (('block_id', 'user_id'),)

class UserFollowHood(models.Model):
    hood = models.ForeignKey(Hood, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = (('hood_id', 'user_id'),)


class Friendship(models.Model):

    from_user = models.ForeignKey(User, related_name='friend_requests_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='friend_requests_received', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=FRIEND_REQUEST_STATUS_CHOICES, default='requested')
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


class Thread(models.Model):
    title = models.CharField(max_length=255)
    # block = models.ForeignKey(Block,  on_delete=models.CASCADE, null=True)
    hood = models.ForeignKey(Hood, on_delete=models.CASCADE, null=True)
    user = models.ManyToManyRel(to=User, field='id', through='UserThread')

    class Meta:
        db_table = 'Thread'

class UserThread(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    # this is a thread where a user might not necessarily be the author, but they are tagged.
    user_id = models.IntegerField()

    class Meta:
        unique_together = (('thread_id', 'user_id'),)

class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    coords = gis_models.PointField(geography=True, srid=4326)
    body = models.TextField()
    datetime = models.DateTimeField(default=models.functions.Now())

class UserAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=models.functions.Now())

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')    
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, null=True)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True)
    friendship = models.ForeignKey(Friendship, on_delete=models.CASCADE, null=True)
    follow = models.ForeignKey(Follow, on_delete=models.CASCADE, null=True)
    datetime = models.DateTimeField(default=models.functions.Now())
    type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
