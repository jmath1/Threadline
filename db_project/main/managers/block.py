from django.db import models

from main.utils.utils import run_query


class BlockManager(models.Manager):

    def get_block_by_id(block_id):
        sql_query = f"""
            SELECT *
            FROM Block
            WHERE block_id = {block_id}
        """
        return run_query(sql_query)

    def get_from_coords(coords):
        sql_query = f"""
            SELECT DISTINCT block_id
            FROM Block b WHERE ST_DWithin({coords}::geography, b.coords::geography, (b.radius)::integer)
        """
        return run_query(sql_query)
    
    def get_member_count(block_id):
        sql_query = f"""
            SELECT COUNT(p.profile_id)
            FROM Profile p
            JOIN Block b ON ST_DWithin(p.coords::geography, b.coords::geography, (b.radius)::integer)
            WHERE b.block_id = {block_id};
        """
        return run_query(sql_query)