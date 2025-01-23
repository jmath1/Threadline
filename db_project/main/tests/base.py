from django.test import TestCase
from django.test import Client
from main.models import User
from unittest.mock import patch

class BaseTestCase(TestCase):
    token = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.geocode_patcher = patch("main.utils.utils.geocode_address")
        cls.mock_geocode_address = cls.geocode_patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.geocode_patcher.stop()
        super().tearDownClass()
        
    def setUp(self):
        self.client = Client()
        self.mock_geocode_address.reset_mock()
        
    def get(self, url, params=None, data=None, auth=False):
        if auth:
            return self.client.get(url, params=params, headers={"Authorization": f"Bearer {self.token}"})

        return self.client.get(url, params=params, data=data)
    
    def post(self, url, params=None, data=None):
        if self.token:
            if params:
                return self.client.post(url, params=params, data=data, headers={"Authorization": f"Bearer {self.token}"})
            return self.client.post(url, params=params, data=data, headers={"Authorization": f"Bearer {self.token}"})
            
        return self.client.post(url, params=params, data=data)
    
    def put(self, url, params=None, data=None):
        if self.token:
            if params:
                return self.client.put(url, params=params, data=data, headers={"Authorization": f"Bearer {self.token}"})
            return self.client.put(url, params=params, data=data, headers={"Authorization": f"Bearer {self.token}"})
            
        return self.client.put(url, params=params, data=data)
    
    def delete(self, url, params=None, data=None, auth=False):
        return self.client.delete(url, params=params, headers={"Authorization": f"Bearer {self.token}"})

    def register_user(
        self, 
        username="newuser", 
        password="password", 
        email="testuser@gmail.com", 
        first_name="Jonathan", 
        last_name="Math", 
        description="required", 
        address="2003 Carpenter St, Philadelphia"
        ):
        
        data = {
            'username': username,
            'password': password,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'description': description,
            'address': address,
        }
        res = self.post('/user/register/', data=data)
        if res.status_code == 201:
            self.token = res.json()["tokens"]["access"]
        else:
            return None
        user = User.objects.get(username=username)
        return user

    def login_user(self, username="newuser", password="password"):
        res = self.post("/api/token/", data={"username": username, "password": password})
        self.token = res.json()["access"]
        return res
    