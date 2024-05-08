from django.db import models

from main.utils.utils import run_query


class UserFollowBlockManager(models.Manager):
    
    def get_follow_by_block_and_user(block_id, user_id):
        sql_query = f"""
            SELECT *
            FROM UserFollowBlock
            WHERE block_id = {block_id} AND user_id = {user_id}
        """
        return run_query(sql_query)
