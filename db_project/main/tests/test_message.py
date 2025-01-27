from django.contrib.gis.geos import Point
from main.factories import MessageFactory
from main.models import Message, Thread
from main.tests.base import BaseTestCase


class MessageTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.mock_geocode_address.return_value = Point(-75.1764407, 39.9404423, srid=4326)
        # Register and log in a test user
        self.user = self.register_user()
        self.login_user()
        # Create a test thread
        self.thread = Thread.objects.create(name="Test Thread", type="general", author=self.user)

    def test_create_message(self):
        """
        Test creating a message in a thread.
        """
        url = f"/api/v1/message/"
        data = {"content": "This is a test message.", "thread_id": self.thread.id}
        response = self.post(url, data=data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Message.objects.count(), 1)
        message = Message.objects.first()
        self.assertEqual(message.content, "This is a test message.")
        self.assertEqual(message.author, self.user)
        self.assertEqual(message.thread, self.thread)

    def test_edit_message(self):
        """
        Test editing a message.
        """
        # Create a message
        message = Message.objects.create(content="Original content", author=self.user, thread=self.thread)

        # Edit the message
        url = f"/api/v1/message/{message.id}/"
        data = {"content": "Updated content"}
        response = self.put(url, data=data)

        self.assertEqual(response.status_code, 200)
        message.refresh_from_db()
        self.assertEqual(message.content, "Updated content")

    def test_delete_message(self):
        """
        Test deleting a message.
        """
        # Create a message
        message = Message.objects.create(content="To be deleted", author=self.user, thread=self.thread)

        # Delete the message
        url = f"/api/v1/message/{message.id}/"
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

    def test_edit_message_permission_denied(self):
        """
        Test editing a message authored by another user.
        """
        # Create a second user and message by them
        message = MessageFactory(content="Their message")

        # Try editing their message
        url = f"/api/v1/message/{message.id}/"
        data = {"content": "Malicious update"}
        response = self.put(url, data=data)

        self.assertEqual(response.status_code, 404)  # User cannot see/edit the message
        message.refresh_from_db()
        self.assertEqual(message.content, "Their message")

    def test_delete_message_permission_denied(self):
        """
        Test deleting a message authored by another user.
        """
        # Create a second user and message by them
        message = MessageFactory()
        # Try deleting their message
        url = f"/api/v1/message/{message.id}/"
        response = self.delete(url)

        self.assertEqual(response.status_code, 404)  # User cannot see/delete the message
        self.assertEqual(Message.objects.count(), 1)
