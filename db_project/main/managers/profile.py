from django.db import models

from main.utils.utils import run_query


class ProfileManager(models.Manager):

    def get(self, username=None):
        sql_query = f"""
            SELECT * FROM PROFILE WHERE username='{username}';
        """
        return run_query(sql_query)[0]
    
    def get_user_id_for_username(self, username=None):
        if username:
            sql_query = f"""
                SELECT user_id FROM PROFILE WHERE username='{username}';
            """
            return run_query(sql_query)[0][0]

    def get_hashed_password(self, username=None):
        if not username:
            return []
        sql_query = f"""
            SELECT password FROM PROFILE WHERE username='{username}';
        """
        return run_query(sql_query)[0][0]
        
        
    def count(self, **kwargs):
        filter_conditions = ""
        if kwargs:
            filter_conditions = " AND ".join([f"{key}='{value}'" for key, value in kwargs.items()])
            filter_conditions = f"WHERE {filter_conditions}"
        sql_query = f"""
            SELECT COUNT(*) FROM Profile {filter_conditions};
        """
        return run_query(sql_query)[0][0]

    def create(self, username, first_name, last_name, email, password, coords, block_id, address, confirmed, description='NULL', photo_url='NULL'):
        import pdb; pdb.set_trace()
        sql_query = f"""INSERT INTO Profile (username, first_name, last_name, block_id, email, password, address, description, photo_url, coords, location_confirmed)
                        VALUES ('{username}', '{first_name}', '{last_name}', '{block_id}','{email}', '{password}', '{address}', '{description}', '{photo_url}', 'POINT{coords}'::geography, '{confirmed}')
                        RETURNING user_id;
                    """
        result = run_query(sql_query)
        if result:
            user_id = result[0][0]
            return user_id
        else:
            return None
        
    def get_profile_by_id(self, profile_id):
        sql_query = f"""
            SELECT *
            FROM Profile
            WHERE user_id = {profile_id};
        """
        return run_query(sql_query)


    def get_profiles_by_block_id(self, block_id):
        sql_query = f"""
            SELECT DISTINCT p.*
            FROM Profile p
            JOIN Block b ON ST_DWithin(p.coords::geography, b.coords::geography, (b.radius)::integer)
            WHERE b.block_id = {block_id};
        """
        return run_query(sql_query)
            
    def get_profiles_by_hood_id(self, hood_id):
        sql_query = f"""
            SELECT DISTINCT p.*
            FROM Profile p
            JOIN Block b ON ST_DWithin(p.coords::geography, b.coords::geography, (b.radius)::integer)
            JOIN Hood h ON h.hood_id = b.hood_id
            WHERE h.hood_id = {hood_id};
        """
        return run_query(sql_query)

