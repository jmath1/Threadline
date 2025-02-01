from django.contrib.gis.geos import Point
from main.factories import ThreadFactory, UserFactory, FriendshipFactory
from main.models import Hood, Thread
from main.tests.base import BaseTestCase


class GetThreadTest(BaseTestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.hood = Hood.objects.get(id=1)
        cls.user.hood = cls.hood
        cls.user.save()
        cls.mock_geocode_address.return_value = Point(-75.1764407, 39.9404423, srid=4326)
        cls.other_hood = Hood.objects.get(id=2)
        
    def setUp(self):
        self.login_user(self.user)
        
    def test_get_hood_thread_allowed(self):
        allowed_hood_thread = ThreadFactory(name="Allowed", hood=self.hood, type="HOOD")
        
        response = self.get(f"/api/v1/thread/{allowed_hood_thread.id}/", auth=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Allowed")
            
    def test_get_hood_thread_not_allowed(self):
        not_allowed_hood_thread = ThreadFactory(name="Not Allowed", hood=self.other_hood, type="HOOD")
        response = self.get(f"/api/v1/thread/{not_allowed_hood_thread.id}/", auth=True)
        self.assertEqual(response.status_code, 403)
        
    def test_get_public_thread(self):
        public_thread = ThreadFactory(name="Public", hood=self.hood, type="PUBLIC")
        response = self.get(f"/api/v1/thread/{public_thread.id}/", auth=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Public")
            
    def test_get_private_thread_participant(self):
        # Create threads in a different neighborhood
        allowed_private_thread = ThreadFactory(name="Allowed Private", hood=self.hood, type="PRIVATE")
        # Add users to the private thread
        allowed_private_thread.participants.add(self.user)
        
        response = self.get(f"/api/v1/thread/{allowed_private_thread.id}/", auth=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Allowed Private")
            
    def test_get_private_thread_not_participant(self):
        not_allowed_private_thread = ThreadFactory(name="Not Allowed Private", type="PRIVATE")
        response = self.get(f"/api/v1/thread/{not_allowed_private_thread.id}/", auth=True)

        self.assertEqual(response.status_code, 403)

class CreateThreadTest(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Set up user and neighborhood
        cls.mock_geocode_address.return_value = Point(-75.1764407, 39.9404423, srid=4326)        
        cls.hood = Hood.objects.get(id=1)
    
    def setUp(self):
        self.login_user(self.user)
    
    def test_create_hood_thread(self):
        data = {
            "name": "Test Thread",
            "type": "HOOD",
            "hood": self.hood.id,
            "content": "Test Content"
        }
        response = self.post("/api/v1/thread/", data=data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Thread.objects.count(), 1)
        self.assertEqual(Thread.objects.get().name, "Test Thread")
        self.assertEqual(Thread.objects.get().type, "HOOD")
        self.assertEqual(Thread.objects.get().hood, self.hood)
        self.assertEqual(Thread.objects.get().author, self.user)
        self.assertEqual(Thread.objects.get().messages.all().count(), 1)
        self.assertEqual(Thread.objects.get().messages.all()[0].author_id, self.user.id)
        self.assertEqual(Thread.objects.get().messages.all()[0].content, "Test Content")
    
    def test_create_public_thread(self):
        data = {
            "name": "Test Thread",
            "type": "PUBLIC",
            "content": "Test Content"
        }
        response = self.post("/api/v1/thread/", data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Thread.objects.count(), 1)
        self.assertEqual(Thread.objects.get().name, "Test Thread")
        self.assertEqual(Thread.objects.get().type, "PUBLIC")
        self.assertEqual(Thread.objects.get().author, self.user)
        self.assertEqual(Thread.objects.get().hood, None)
        self.assertEqual(Thread.objects.get().messages.all().count(), 1)
        self.assertEqual(Thread.objects.get().messages.all()[0].author_id, self.user.id)
        self.assertEqual(Thread.objects.get().messages.all()[0].content, "Test Content")
        
    def test_create_private_thread(self):
        user_2 = UserFactory(username="user2", email="test2@gmail.com")
        FriendshipFactory(from_user=self.user, to_user=user_2, status="ACCEPTED")
        data = {
            "name": "Test Thread",
            "type": "PRIVATE",
            "content": "Test Content @user2"
        }
        response = self.post("/api/v1/thread/", data=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Thread.objects.count(), 1)
        self.assertEqual(Thread.objects.get().name, "Test Thread")
        self.assertEqual(Thread.objects.get().type, "PRIVATE")
        self.assertEqual(Thread.objects.get().author, self.user)
        self.assertEqual(Thread.objects.get().participants.all().count(), 2)
  
class DeleteThreadTest(BaseTestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mock_geocode_address.return_value = Point(-75.1764407, 39.9404423, srid=4326)

    def setUp(self):
        super().setUp()
        self.login_user(self.user)
        
    def test_author_delete_thread(self):
        thread = ThreadFactory(name="Test Thread", author=self.user)
        res = self.delete(f"/api/v1/thread/{thread.id}/")
        self.assertEqual(res.status_code, 204)
        self.assertEqual(Thread.objects.count(), 0)
        
    def test_author_not_delete_thread(self):
        thread = ThreadFactory(name="Test Thread")
        res = self.delete(f"/api/v1/thread/{thread.id}/")
        self.assertEqual(res.status_code, 403)
        self.assertEqual(Thread.objects.count(), 1)
        
    def test_thread_not_found(self):
        res = self.delete(f"/api/v1/thread/999/")
        self.assertEqual(res.status_code, 404)
        self.assertEqual(Thread.objects.count(), 0)
        