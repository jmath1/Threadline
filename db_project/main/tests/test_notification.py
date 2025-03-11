from unittest.mock import patch

from django.contrib.gis.geos import Point
from main.factories import (FollowFactory, FriendshipFactory, MessageFactory,
                            ThreadFactory, UserFactory)
from main.models import Tag
from main.tasks import create_notification
from main.tests.base import BaseTestCase


class NotificationSignalTests(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mock_geocode_address.return_value = Point(-75.1764407, 39.9404423, srid=4326)

    def setUp(self):
        self.user2 = UserFactory(username="user2")
        self.tagged_user = UserFactory(username="tagged_user", id=3)
        self.thread = ThreadFactory(author=self.user2)
    
    @patch("main.tasks.create_notification.delay")
    def test_notify_friend_request(self, mock_create_notification):
        """Test that a FRIEND_REQUESTED notification is created on friend request"""
        friendship = FriendshipFactory(from_user=self.user, to_user=self.user2, status="REQUESTED")

        mock_create_notification.assert_called_once_with(
            user_id=self.user2.id,
            notification_type="FRIEND_REQUESTED",
            related_model="friendship",
            related_model_id=friendship.id
        )

    @patch("main.tasks.create_notification.delay")
    def test_notify_friend_acceptance(self, mock_create_notification):
        """Test that a FRIEND_ACCEPTED notification is sent when a request is accepted"""
        friendship = FriendshipFactory(from_user=self.user, to_user=self.user2, status="ACCEPTED")

        mock_create_notification.assert_called_once_with(
            user_id=self.user.id,
            notification_type="FRIEND_ACCEPTED",
            related_model="friendship",
            related_model_id=friendship.id
        )

    @patch("main.tasks.create_notification.delay")
    def test_notify_follower(self, mock_create_notification):
        """Test that a FOLLOW notification is created when a user follows another"""
        follow = FollowFactory(follower=self.user, followee=self.user2)

        mock_create_notification.assert_called_once_with(
            user_id=self.user2.id,
            notification_type="FOLLOW",
            related_model="follow",
            related_model_id=follow.id
        )

