from unittest.mock import patch

from django.conf import settings
from main.factories import UserFactory
from main.models import Message, User
from pymongo import MongoClient
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


class BaseTestCase(APITestCase):
    token = None
    mongo_client = None
    mongo_db = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Set up MongoDB test database
        cls.mongo_client = MongoClient(f"mongodb://{settings.MONGO_HOST}:27017/")
        cls.mongo_db = cls.mongo_client["test"]
        Message._meta["db_alias"] = "test"  # Set test DB alias for mongoengine
        cls.mongo_db["messages"].delete_many({})  # Ensure the test collection is clean

        cls.user = UserFactory(username="user1", email="user1@gmail.com")

        cls.geocode_patcher = patch("main.utils.utils.geocode_address")
        cls.mock_geocode_address = cls.geocode_patcher.start()
    
    def tearDown(self):
        Message.objects.all().delete() 
        self.mock_geocode_address.reset_mock()
        super().tearDown()
        
    @classmethod
    def tearDownClass(cls):
        cls.mongo_client.drop_database("test")
        cls.mongo_client.close()
        cls.geocode_patcher.stop()
        super().tearDownClass()
        
    def setUp(self):
        self.mongo_db["messages"].delete_many({}) 
        self.mock_geocode_address.reset_mock()
        
    def get(self, url, params=None, data=None, auth=False):
        if auth:
            return self.client.get(url, params=params, headers={"Authorization": f"Bearer {self.token}"})

        return self.client.get(url, params=params, data=data)
    
    def post(self, url, params=None, data=None):
       
        if self.token:
            if params:
                res = self.client.post(url, params=params, data=data, headers={"Authorization": f"Bearer {self.token}"})
            res = self.client.post(url, data=data, headers={"Authorization": f"Bearer {self.token}"})
        else:
            res = self.client.post(url, params=params, data=data)
    
        if res.status_code == 400:
            print(res.json())
        return res

    def put(self, url, params=None, data=None):
        if self.token:
            if params:
                return self.client.put(url, params=params, data=data, headers={"Authorization": f"Bearer {self.token}"})
            return self.client.put(url, data=data, headers={"Authorization": f"Bearer {self.token}"}, content_type="application/json",)
            
        return self.client.put(url, params=params, data=data)
    
    def delete(self, url):
        return self.client.delete(url, headers={"Authorization": f"Bearer {self.token}"})

    def register_user(
        self, 
        username="newuser", 
        password="password", 
        email="testuser@gmail.com", 
        first_name="Jonathan", 
        last_name="Math", 
        address="Next St, New York"
        ):
        
        data = {
            'username': username,
            'password': password,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'address': address,
        }
        res = self.post('/api/v1/user/register/', data=data)
        if res.status_code == 201:
            self.token = res.json()["tokens"]["access"]
        else:
            return None
        user = User.objects.get(username=username)
        return user

    def get_auth_token(self, user):
        """Generate a token for the given user without hitting the endpoint."""
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    def login_user(self, user):
        token = self.get_auth_token(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
