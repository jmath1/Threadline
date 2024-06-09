from django.db import models
from main.utils.utils import run_query


class HoodManager(models.Manager):

    def get_hood_by_id(hood_id):
        sql_query = f"""
            SELECT *
            FROM Hood
            WHERE hood_id = {hood_id}
        """
        return run_query(sql_query)
