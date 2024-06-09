from django.db import models
from main.utils.utils import run_query


class UserFollowHoodManager(models.Manager):
    
    def get_follow_by_hood_and_user(hood_id, user_id):
        sql_query = f"""
            SELECT *
            FROM UserFollowHood
            WHERE hood_id = {hood_id} AND user_id = {user_id}
        """
        return run_query(sql_query)

