from django.contrib.gis.geos import Point
from django.urls import reverse
from main.models import Follow
from main.tests.base import BaseTestCase


class TestFollow(BaseTestCase):
    def test_following(self):
        self.mock_geocode_address.return_value = Point(-75.1764407, 39.9404423, srid=4326)
        user_1 = self.register_user(username="newuser1", password="password1")
        user_2 = self.register_user(username="newuser2", email="user2@example.com", password="password2")
        
        # First user follows the second user
        self.login_user(username="newuser1", password="password1")
        url = url = reverse("follow", kwargs={"followee_id": user_2.pk})
        res = self.post(url)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(Follow.objects.count(), 1)
        
        # Second user checks if they now have one follower
        self.login_user(username="newuser2", password="password2")
        user_info = self.get(f"/api/v1/user/me/", auth=True).json()
        self.assertEqual(user_info.get('friends_count'), 0)
        self.assertEqual(user_info.get('followers_count'), 1)
        
        # Second user lists lists their followers
        res = self.get("/api/v1/follow/followers/", auth=True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()), 1)
        self.assertEqual(res.json()[0]['username'], "newuser1")
        
        # First user unfollows the second user
        self.login_user(username="newuser1", password="password1")
        res = self.post(f"/api/v1/follow/unfollow/{user_2.pk}")
        self.assertEqual(res.status_code, 204)
        self.assertEqual(Follow.objects.count(), 0)
        