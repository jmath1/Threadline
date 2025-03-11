from django.contrib.gis.geos import Point
from django.urls import reverse
from main.factories import UserFactory
from main.models import Friendship, User
from main.tests.base import BaseTestCase


class TestFriendship(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mock_geocode_address.return_value = Point(-75.1764407, 39.9404423, srid=4326) 
        cls.user_2 = UserFactory(username="user2", email="user2@example.com", password="password2")
    
    def test_send_friend_request(self):
        self.login_user(self.user)
        url = "/api/v1/friendship/requests/"
        res = self.post(url, data={"to_user": self.user_2.id})
        self.assertEqual(res.status_code, 201)
        self.assertEqual(Friendship.objects.count(), 1)
        
    def test_list_friend_requests(self):
        friendship = Friendship.objects.create(from_user=self.user, to_user=self.user_2, status="REQUESTED")
        self.login_user(self.user_2)
        url = f"/api/v1/friendship/requests/"
        res = self.get(url, auth=True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()), 1)
        self.assertEqual(res.json()[0]["from_user"]["username"], "user1")
    
    def test_accept_friend_request(self):
        friendship = Friendship.objects.create(from_user=self.user, to_user=self.user_2, status="REQUESTED")
        self.login_user(self.user_2)
        url = f"/api/v1/friendship/accept/{friendship.pk}/"
        res = self.post(url)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(Friendship.objects.filter(to_user=self.user_2.pk, from_user=self.user.pk).exists())
        self.assertTrue(Friendship.objects.get(to_user=self.user_2.pk, from_user=self.user.pk).status=="ACCEPTED")
    
    def test_reject_friend_request(self):
        friendship = Friendship.objects.create(from_user=self.user, to_user=self.user_2, status="REQUESTED")
        self.login_user(self.user_2)
        url = f"/api/v1/friendship/reject/{friendship.pk}/"
        res = self.post(url)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(Friendship.objects.filter(to_user=self.user_2.pk, from_user=self.user.pk).exists())
        self.assertTrue(Friendship.objects.get(to_user=self.user_2.pk, from_user=self.user.pk).status=="REJECTED")
        
    
    def test_remove_friend(self):
        self.login_user(self.user)
        friendship = Friendship.objects.create(from_user=self.user, to_user=self.user_2, status="ACCEPTED")
        url = f"/api/v1/friendship/remove/{friendship.pk}/"
        res = self.delete(url)
        self.assertEqual(res.status_code, 204)
        self.assertFalse(Friendship.objects.filter(to_user=self.user_2, from_user=self.user).exists())
        self.assertFalse(Friendship.objects.filter(to_user=self.user, from_user=self.user_2).exists())
        self.assertEqual(Friendship.objects.count(), 0)