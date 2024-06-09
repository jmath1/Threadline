# Create your models here.
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.gis.db import models as gis_models
from django.db import models
from main.managers import *
from main.utils.utils import run_query


class Hood(models.Model):
    hood_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    objects = HoodManager()

    class Meta:
        managed = False
        db_table = 'Hood'

class Block(models.Model):
    block_id = models.IntegerField(primary_key=True)
    hood = models.ForeignKey(Hood, on_delete=models.CASCADE)
    description = models.TextField()
    name = models.CharField(max_length=100, unique=True)
    coords = gis_models.PointField(geography=True)
    radius = models.DecimalField(max_digits=10, decimal_places=6)
    
    objects = BlockManager()

    class Meta:
        managed = False
        db_table = 'Block'

class Profile(AbstractBaseUser):
    user_id = models.IntegerField(primary_key=True,)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    description = models.TextField()
    photo_url = models.CharField(max_length=255)
    coords = gis_models.PointField(geography=True)
    location_confirmed = models.BooleanField()
    
    objects = ProfileManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'password', 'first_name', 'last_name']
    is_anonymous = False
    class Meta:
        managed = False
        db_table = 'profile'

    @property
    def is_authenticated(self):
        return True
    
    def get_profile_hood_and_block(self):
        sql_query = f"""
            SELECT b.name AS block_name, b.hood_id
            FROM Profile p
            JOIN Block b ON ST_DWithin(p.coords::geography, b.coords::geography, b.radius)
            WHERE p.user_id = {self.user_id};
        """
        return run_query(sql_query)

    def confirm_location(self, block_id):
        confirmed = False
        if self.get_member_count(block_id) <= 3:
            confirmed = True
        else:
            # count profile block approvals for block_id and profile_id
            if ProfileBlockApproval.objects.count(block_id, self.user_id) >= 3:
                confirmed = True
        self.location_confirmed = confirmed
        self.save()

    class Meta:
        managed = False
        db_table = 'Profile'

class ProfileBlockApproval(models.Model):
    block_id = models.IntegerField()
    user_id = models.IntegerField()
    approver_id = models.IntegerField()

    objects = ProfileBlockApprovalManager()
    class Meta:
        managed = False
        db_table = 'ProfileBlockApproval'
        unique_together = (('block_id', 'user_id', 'approver_id'),)

class UserFollowBlock(models.Model):
    block_id = models.IntegerField()
    user_id = models.IntegerField()
    
    objects = UserFollowBlockManager()

    class Meta:
        managed = False
        db_table = 'UserFollowBlock'
        unique_together = (('block_id', 'user_id'),)

class UserFollowHood(models.Model):
    hood_id = models.IntegerField()
    user_id = models.IntegerField()
    
    objects = UserFollowHoodManager()

    class Meta:
        managed = False
        db_table = 'UserFollowHood'
        unique_together = (('hood_id', 'user_id'),)

class Friendship(models.Model):
    follower_id = models.IntegerField()
    followee_id = models.IntegerField()
    confirmed = models.BooleanField()
    
    objects = FriendshipManager()

    class Meta:
        managed = False
        db_table = 'Friendship'
        unique_together = (('follower_id', 'followee_id'),)

class Thread(models.Model):
    thread_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    block_id = models.IntegerField(null=True)
    hood_id = models.IntegerField(null=True)
    
    objects = ThreadManager()

    class Meta:
        managed = False
        db_table = 'Thread'

class UserThread(models.Model):
    thread_id = models.IntegerField()
    user_id = models.IntegerField()
    
    objects = UserThreadManager()

    class Meta:
        managed = False
        db_table = 'UserThread'
        unique_together = (('thread_id', 'user_id'),)

class Message(models.Model):
    message_id = models.IntegerField(primary_key=True)
    thread_id = models.IntegerField()
    user_id = models.IntegerField()
    coords = gis_models.PointField(geography=True)
    body = models.TextField()
    datetime = models.DateTimeField(default=models.functions.Now())
    
    objects = MessageManager()

    class Meta:
        managed = False
        db_table = 'Message'

class UserAccess(models.Model):
    user_id = models.IntegerField()
    thread_id = models.IntegerField(null=True)
    datetime = models.DateTimeField(default=models.functions.Now())
    
    objects = UserAccessManager()

    class Meta:
        managed = False
        db_table = 'UserAccess'

class Notifications(models.Model):
    notification_id = models.AutoField(primary_key=True)
    to_user = models.IntegerField()
    user_id = models.IntegerField()
    notification_type = models.CharField(max_length=50)
    thread_id = models.IntegerField(null=True)
    message_id = models.IntegerField(null=True)
    datetime = models.DateTimeField(default=models.functions.Now())
    
    objects = NotificationsManager()

    class Meta:
        managed = False
        db_table = 'Notifications'
