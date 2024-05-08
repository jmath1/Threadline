from django.db import models

from main.utils.utils import run_query


class FriendshipManager(models.Manager):
    
    def get_friendship(follower_id, followee_id):
        sql_query = f"""
            SELECT *
            FROM Friendship
            WHERE follower_id = {follower_id} AND followee_id = {followee_id}
        """
        return run_query(sql_query)

