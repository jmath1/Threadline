from django.db import models
from main.utils.utils import run_query


class UserAccessManager(models.Manager):
    
    def get_user_access(user_id, thread_id):
        sql_query = f"""
            SELECT *
            FROM UserAccess
            WHERE user_id = {user_id} AND thread_id = {thread_id}
        """
        return run_query(sql_query)
