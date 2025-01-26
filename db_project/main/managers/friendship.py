from django.db import models


class FriendshipManager(models.Manager):
    
    def get_friendship(self, follower_id, followee_id):    
        return self.objects.filter(follower_id=follower_id, followee_id=followee_id)

