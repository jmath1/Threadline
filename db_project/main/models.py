from django.db import models

# Create your models here.
from django.contrib.gis.db import models

class Hood(models.Model):
    hood_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        managed = False
        db_table = 'Hood'

class Block(models.Model):
    block_id = models.IntegerField(primary_key=True)
    hood = models.ForeignKey(Hood, on_delete=models.CASCADE)
    description = models.TextField()
    name = models.CharField(max_length=100, unique=True)
    coords = models.PointField(geography=True)
    radius = models.DecimalField(max_digits=10, decimal_places=6)

    class Meta:
        managed = False
        db_table = 'Block'

class Profile(models.Model):
    user_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    description = models.TextField()
    photo_url = models.CharField(max_length=255)
    coords = models.PointField(geography=True)
    location_confirmed = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'Profile'

class ProfileBlockApproval(models.Model):
    block_id = models.IntegerField()
    user_id = models.IntegerField()
    approver_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ProfileBlockApproval'
        unique_together = (('block_id', 'user_id', 'approver_id'),)

class UserFollowBlock(models.Model):
    block_id = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'UserFollowBlock'
        unique_together = (('block_id', 'user_id'),)

class UserFollowHood(models.Model):
    hood_id = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'UserFollowHood'
        unique_together = (('hood_id', 'user_id'),)

class Friendship(models.Model):
    follower_id = models.IntegerField()
    followee_id = models.IntegerField()
    confirmed = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'Friendship'
        unique_together = (('follower_id', 'followee_id'),)

class Thread(models.Model):
    thread_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    block_id = models.IntegerField(null=True)
    hood_id = models.IntegerField(null=True)

    class Meta:
        managed = False
        db_table = 'Thread'

class UserThread(models.Model):
    thread_id = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'UserThread'
        unique_together = (('thread_id', 'user_id'),)

class Message(models.Model):
    message_id = models.IntegerField(primary_key=True)
    thread_id = models.IntegerField()
    user_id = models.IntegerField()
    coords = models.PointField(geography=True)
    body = models.TextField()
    datetime = models.DateTimeField(default=models.functions.Now())

    class Meta:
        managed = False
        db_table = 'Message'

class UserAccess(models.Model):
    user_id = models.IntegerField()
    thread_id = models.IntegerField(null=True)
    datetime = models.DateTimeField(default=models.functions.Now())

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

    class Meta:
        managed = False
        db_table = 'Notifications'
