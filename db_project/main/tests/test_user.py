from django.contrib.gis.geos import Point
from main.models import User
from main.tests.base import BaseTestCase


class TestRegistration(BaseTestCase):
    def test_register_new_user(self):     
        self.mock_geocode_address.return_value = Point(-75.1764407, 39.9404423, srid=4326)   
        res = self.register_user()
        # # Add assertions to verify that the user was created as expected
        self.assertEqual(User.objects.count(), 1)
        res = self.get("/api/v1/user/me/", auth=True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["username"], "newuser")

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
        self.assertEqual(User.objects.count(), 0)

    def test_invalid_username(self):
        self.mock_geocode_address.return_value = Point(-75.1764407, 39.9404423, srid=4326)
        self.register_user(username="newuser")
        user = self.register_user(username="newuser")
        self.assertEqual(user, None)


class TestAuthentication(BaseTestCase):
    def test_good_login(self):
        self.mock_geocode_address.return_value = Point(-75.1764407, 39.9404423, srid=4326)
        res = self.register_user()
        res = self.login_user()
        self.assertEqual(res.status_code, 200)
        
    def test_bad_login(self):
        self.mock_geocode_address.return_value = Point(-75.1764407, 39.9404423, srid=4326)
        self.register_user()
        res = self.post("/api/v1/token/", data={"username": "newuser", "password": "badpassword"})
        self.assertEqual(res.status_code, 401)
        
class TestEditUser(BaseTestCase):
    
    def test_unauth(self):
        res = self.post("/api/v1/user/edit/", data={"first_name": "newname", "last_name": "newlast", "description": "newdesc", "address": "334 Amsterdam Ave W 76th St, New York"})
        self.assertEqual(res.status_code, 401)
    
    def test_user_edit_success(self):
        self.mock_geocode_address.return_value = Point(-75.1764407, 39.9404423, srid=4326)
        self.register_user()
        self.login_user()
        res = self.post("/api/v1/user/edit/", data={"username": "backagain","first_name": "newname", "last_name": "newlast", "description": "newdesc", "address": "931 Federal St, Philadelphia"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(User.objects.get(username="backagain").first_name, "newname")
