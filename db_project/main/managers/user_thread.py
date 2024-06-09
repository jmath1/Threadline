from django.db import models
from main.utils.utils import run_query


class UserThreadManager(models.Manager):
    
    def get_user_thread(thread_id, user_id):
        sql_query = f"""
            SELECT *
            FROM UserThread
            WHERE thread_id = {thread_id} AND user_id = {user_id}
        """
        return run_query(sql_query)
