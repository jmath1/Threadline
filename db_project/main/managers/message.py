from django.db import models

from main.utils.utils import run_query


class MessageManager(models.Manager):
    
    def get_message_by_id(message_id):
        sql_query = f"""
            SELECT *
            FROM Message
            WHERE message_id = {message_id}
        """
        return run_query(sql_query)
