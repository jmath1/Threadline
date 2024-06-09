from django.db import models
from main.utils.utils import run_query


class ProfileBlockApprovalManager(models.Manager):

    def count(block_id, user_id):
        sql_query = f"""
            SELECT COUNT(*)
            FROM ProfileBlockApproval
            WHERE block_id = {block_id} AND user_id = {user_id}
        """
        return run_query(sql_query)
