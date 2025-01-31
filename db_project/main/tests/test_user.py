from django.contrib.gis.geos import Point
from main.models import User
from main.tests.base import BaseTestCase


class TestRegistration(BaseTestCase):

    def test_register_user(self):
        self.mock_geocode_address.return_value = Point(-75.1764407, 39.9404423, srid=4326)
        data = {
            'username': 'username',
            'password': 'password',
            'email': 'email@gmail.com',
            'first_name': 'firstname',
            'last_name': 'lastname',
            'description': 'description',
            'address': 'address',
        }
        res = self.post('/api/v1/user/register/', data=data)
        self.assertEqual(res.status_code, 201)
        self.assertTrue(res.json()["tokens"]["access"] is not None)
        user = User.objects.filter(username='username')
        self.assertEqual(user.count(), 1)
    
    def test_me(self):     
        self.login_user(self.user)
        res = self.get("/api/v1/user/me/", auth=True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["username"], "user1")

    def test_register_unsupported_hood(self):
        data = {
            'username': 'anotheruser', 
            'password': 'password', 
            'email': 'anotheruser@gmail.com',
            'first_name': 'Jonathan',
            'last_name': 'Math',
            'description': 'required',
            'address': '34 2nd St',
        }
        self.mock_geocode_address.return_value = None
        res = self.post('/api/v1/user/register/', data=data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json(), ["Hood not supported"])
        self.assertEqual(User.objects.filter(username='anotheruser').count(), 0)

    def test_invalid_username(self):
        self.mock_geocode_address.return_value = Point(-75.1764407, 39.9404423, srid=4326)
        data = {
            'username': 'user1',
            'password': 'password',
            'email': 'email@gmail.com',
            'first_name': 'first_name',
            'last_name': 'last_name',
            'description': 'description',
            'address': 'address',
        }
        res = self.post('/api/v1/user/register/', data=data)
        self.assertEqual(res.status_code, 400)

class TestAuthentication(BaseTestCase):
    def test_good_login(self):
        self.mock_geocode_address.return_value = Point(-75.1764407, 39.9404423, srid=4326)
        res = self.post("/api/v1/token/", data={"username": self.user.username, "password": 'password'})
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json().get("access") is not None)
        
    def test_bad_login(self):
        self.mock_geocode_address.return_value = Point(-75.1764407, 39.9404423, srid=4326)
        res = self.post("/api/v1/token/", data={"username": "user1", "password": "badpassword"})
        self.assertEqual(res.status_code, 401)
        
class TestEditUser(BaseTestCase):
    
    def test_unauth(self):
        res = self.post("/api/v1/user/edit/", data={"first_name": "newname", "last_name": "newlast", "description": "newdesc", "address": "334 Amsterdam Ave W 76th St, New York"})
        self.assertEqual(res.status_code, 401)
    
    def test_user_edit_success(self):
        self.mock_geocode_address.return_value = Point(-75.1764407, 39.9404423, srid=4326)
        
        self.login_user(self.user)
        res = self.post("/api/v1/user/edit/", data={"username": "backagain","first_name": "newname", "last_name": "newlast", "description": "newdesc", "address": "931 Federal St, Philadelphia"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(User.objects.get(username="backagain").first_name, "newname")
