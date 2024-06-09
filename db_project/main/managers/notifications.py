from django.db import models
from main.utils.utils import run_query


class NotificationsManager(models.Manager):
    
    def get_notification_by_id(notification_id):
        sql_query = f"""
            SELECT *
            FROM Notifications
            WHERE notification_id = {notification_id}
        """
        return run_query(sql_query)
