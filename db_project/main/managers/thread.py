from django.db import models
from main.utils.utils import run_query


class ThreadManager(models.Manager):
    
    def get_thread_by_id(thread_id):
        sql_query = f"""
            SELECT *
            FROM Thread
            WHERE thread_id = {thread_id}
        """
        return run_query(sql_query)
