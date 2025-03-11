import json

import redis
from django.conf import settings
from django.contrib.gis.geos import Point
from main.factories import (FriendshipFactory, MessageFactory, ThreadFactory,
                            UserFactory)
from main.models import Message, Thread
from main.tests.base import BaseTestCase


class MessageTests(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mock_geocode_address.return_value = Point(-75.1764407, 39.9404423, srid=4326)
    
    def setUp(self):
        Thread.objects.all().delete()
        self.thread = Thread.objects.create(name="Test Thread", type="general", author_id=self.user.id)
        self.login_user(self.user)
        
    def test_create_message_public(self):
        """
        Test creating a message in a thread.
        """
        url = f"/api/v1/message/"
        data = {"content": "This is a test message.", "thread_id": self.thread.id}
        self.thread.participants.add(self.user)
        response = self.post(url, data=data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Message.objects.count(), 1)
        message = Message.objects.first()
        self.assertEqual(message.content, "This is a test message.")
        self.assertEqual(message.author_id, self.user.id)
        self.assertEqual(message.thread_id, self.thread.id)

    def test_edit_message(self):
        """
        Test editing a message.
        """
        # Create a message
        message = Message.objects.create(content="Original content", author_id=self.user.id, thread_id=self.thread.id)

        # Edit the message
        url = f"/api/v1/message/{message.external_id}/"
        data = {"content": "Updated content"}
        response = self.put(url, data=data)

        self.assertEqual(response.status_code, 200)
        message = Message.objects.first()
        self.assertEqual(message.content, "Updated content")

    def test_delete_message(self):
        """
        Test deleting a message.
        """
        # Create a message
        message = Message.objects.create(content="To be deleted", author_id=self.user.id, thread_id=self.thread.id)
        # Delete the message
        url = f"/api/v1/message/{message.external_id}/"
        response = self.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Message.objects.count(), 0)

    def test_create_message_invalid_thread(self):
        """
        Test creating a message in a non-existent thread.
        """
        url = "/api/v1/message/"
        data = {"content": "This will fail.", "thread_id": 99999}
        response = self.post(url, data=data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Message.objects.count(), 0)
        self.assertEqual(response.json(), {'detail': 'No Thread matches the given query.'})

    def test_create_message_private_thread_non_participant(self):
        """
        Test creating a message in a private thread that the user does not participate in
        """
        url = "/api/v1/message/"
        thread = ThreadFactory(name="Private Thread", type="PRIVATE")
        data = {"content": "This will fail.", "thread_id": thread.id}
        response = self.post(url, data=data)
        self.assertEqual(response.status_code, 403)
        
    def test_create_message_private_thread_participant(self):
        """
        Test creating a message in a private thread that the user participates in
        """
        url = "/api/v1/message/"
        thread = ThreadFactory(name="Private Thread", type="PRIVATE")
        thread.participants.add(self.user)
        data = {"content": "This will succeed.", "thread_id": thread.id}
        response = self.post(url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Message.objects.count(), 1)
        message = Message.objects.first()
        self.assertEqual(message.content, "This will succeed.")
        self.assertEqual(message.author_id, self.user.id)
        self.assertEqual(message.thread_id, thread.id)
            
    def test_create_message_non_hood_member(self):
        """
        Test creating a message in a thread in a hood that the user is not a member of.
        """
        url = "/api/v1/message/"
        thread = ThreadFactory(name="Hood Thread")
        data = {"content": "This will fail.", "thread_id": thread.id}
        response = self.post(url, data=data)
        self.assertEqual(response.status_code, 403)
    
        
    def test_edit_message_permission_denied(self):
        """
        Test editing a message authored by another user.
        """
        # Create a second user and message by them
        message = MessageFactory(content="Their message")

        # Try editing their message
        url = f"/api/v1/message/{message.external_id}/"
        data = {"content": "Malicious update"}
        response = self.put(url, data=data)

        self.assertEqual(response.status_code, 403)  # User cannot see/edit the message
        message = Message.objects.first()
        self.assertEqual(message.content, "Their message")

    def test_delete_message_permission_denied(self):
        """
        Test deleting a message authored by another user.
        """
        # Create a second user and message by them
        message = MessageFactory()
        # Try deleting their message
        url = f"/api/v1/message/{message.external_id}/"
        response = self.delete(url)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Message.objects.count(), 1)

    # test Restrict thread/message tagging to users that the author is friends with.
    def test_tagging_friends_allowed(self):
        """
        Test tagging a friend in a message.
        """
        friend = UserFactory(username='friend')
        thread = ThreadFactory(author=self.user, hood=None)
        thread.participants.add(self.user)
        friendship = FriendshipFactory(from_user=self.user, to_user=friend, status="ACCEPTED")
        url = f"/api/v1/message/"
        data = {"content": "Hello @friend", "thread_id": thread.id}
        response = self.post(url, data=data)
        self.assertEqual(response.status_code, 201)
        message = Message.objects.first()
        
        self.assertEqual(message.tags[0].username, 'friend')
        self.assertEqual(message.content, "Hello @friend")
        self.assertEqual(message.author_id, self.user.id)
        self.assertEqual(message.thread_id, thread.id)
        self.assertEqual(message.tags[0].user_id, friend.id)
        thread.refresh_from_db()
        self.assertEqual(thread.participants.count(), 2)
        redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
        self.assertEqual(redis_client.llen(f"notifications:user:{friend.id}"), 1)
        notification = json.loads(redis_client.lpop(f"notifications:user:{friend.id}"))
        self.assertEqual(notification['message_id'], message.external_id)
        self.assertEqual(notification['thread_id'], thread.id)
        self.assertEqual(notification['message_id'], message.external_id)
        self.assertEqual(notification['type'], "TAGGED")
        
    def test_tagging_not_friend_not_allowed(self):
        """
        Test that friends are not allowed to tag users that are not their friends
        """
        other_user = UserFactory(username='other_user')
        thread = ThreadFactory(author=self.user, type="PRIVATE")
        thread.participants.add(self.user)
        url = f"/api/v1/message/"
        data = {"content": "Hello @other_user", "thread_id": thread.id}
        response = self.post(url, data=data)
        self.assertEqual(response.status_code, 201)
        message = Message.objects.first()
        self.assertTrue(len(message.tags) == 0 )
        self.assertEqual(message.content, "Hello @other_user")
        self.assertEqual(message.author_id, self.user.id)
        self.assertEqual(message.thread_id, thread.id)
        self.assertEqual(thread.participants.count(), 1)
        self.assertEqual(thread.participants.first(), self.user)
        