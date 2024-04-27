from django.db import models
from main.utils import run_query


class ProfileBlockApprovalManager(models.Manager):

    def count(block_id, user_id):
        sql_query = f"""
            SELECT COUNT(*)
            FROM ProfileBlockApproval
            WHERE block_id = {block_id} AND user_id = {user_id}
        """
        return run_query(sql_query)


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

class HoodManager(models.Manager):

    def get_hood_by_id(hood_id):
        sql_query = f"""
            SELECT *
            FROM Hood
            WHERE hood_id = {hood_id}
        """
        return run_query(sql_query)


class ProfileManager(models.Manager):

    def create(self, username, first_name, last_name, email, password, coords, description=None, photo_url=None):
        sql_query = f"""
            INSERT INTO Profile (username, first_name, last_name, email, password, description, photo_url, coords, location_confirmed)
            VALUES ('{username}', '{first_name}', '{last_name}', '{email}', '{password}', '{description}', '{photo_url}', ST_GeomFromText('{coords}', 4326), '{location_confirmed}')
            RETURNING user_id;
        """
        result = run_query(sql_query)
        if result:
            user_id = result[0][0]
            return self.get(user_id=user_id)
        else:
            return None
        
    def get_profile_by_id(profile_id):
        sql_query = f"""
            SELECT *
            FROM Profile
            WHERE user_id = {profile_id}
        """
        return run_query(sql_query)
    
    def get_profiles_by_block_id(block_id):
        sql_query = f"""
            SELECT DISTINCT p.*
            FROM Profile p
            JOIN Block b ON ST_DWithin(p.coords::geography, b.coords::geography, (b.radius)::integer)
            WHERE b.block_id = {block_id};
        """
        return run_query(sql_query)
            
    def get_profiles_by_hood_id(hood_id):
        sql_query = f"""
            SELECT DISTINCT p.*
            FROM Profile p
            JOIN Block b ON ST_DWithin(p.coords::geography, b.coords::geography, (b.radius)::integer)
            JOIN Hood h ON h.hood_id = b.hood_id
            WHERE h.hood_id = {hood_id};
        """
        return run_query(sql_query)


class UserFollowBlockManager(models.Manager):
    
    def get_follow_by_block_and_user(block_id, user_id):
        sql_query = f"""
            SELECT *
            FROM UserFollowBlock
            WHERE block_id = {block_id} AND user_id = {user_id}
        """
        return run_query(sql_query)


class UserFollowHoodManager(models.Manager):
    
    def get_follow_by_hood_and_user(hood_id, user_id):
        sql_query = f"""
            SELECT *
            FROM UserFollowHood
            WHERE hood_id = {hood_id} AND user_id = {user_id}
        """
        return run_query(sql_query)


class FriendshipManager(models.Manager):
    
    def get_friendship(follower_id, followee_id):
        sql_query = f"""
            SELECT *
            FROM Friendship
            WHERE follower_id = {follower_id} AND followee_id = {followee_id}
        """
        return run_query(sql_query)


class ThreadManager(models.Manager):
    
    def get_thread_by_id(thread_id):
        sql_query = f"""
            SELECT *
            FROM Thread
            WHERE thread_id = {thread_id}
        """
        return run_query(sql_query)


class UserThreadManager(models.Manager):
    
    def get_user_thread(thread_id, user_id):
        sql_query = f"""
            SELECT *
            FROM UserThread
            WHERE thread_id = {thread_id} AND user_id = {user_id}
        """
        return run_query(sql_query)


class MessageManager(models.Manager):
    
    def get_message_by_id(message_id):
        sql_query = f"""
            SELECT *
            FROM Message
            WHERE message_id = {message_id}
        """
        return run_query(sql_query)


class UserAccessManager(models.Manager):
    
    def get_user_access(user_id, thread_id):
        sql_query = f"""
            SELECT *
            FROM UserAccess
            WHERE user_id = {user_id} AND thread_id = {thread_id}
        """
        return run_query(sql_query)


class NotificationsManager(models.Manager):
    
    def get_notification_by_id(notification_id):
        sql_query = f"""
            SELECT *
            FROM Notifications
            WHERE notification_id = {notification_id}
        """
        return run_query(sql_query)
