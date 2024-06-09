from unittest.mock import MagicMock, patch

from django.test import Client, TestCase
from main.models import Profile


class BaseTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.token = None
    
    def get(self, url, params=None, data=None, auth=False):
        if auth:
            return self.client.get(url, params=params, headers={"Authorization": f"{self.token}"})

        return self.client.get(url, params=params, data=data)
    
    def post(self, url, params=None, data=None):
        return self.client.post(url, params=params, data=data, headers={"Authorization": f"{self.token}"})
            
    def delete(self, url, params=None, data=None, auth=False):
        return self.client.delete(url, params=params, headers={"Authorization": f"{self.token}"})

    
    def register_user(
        self, 
        username="newuser", 
        password="password", 
        email="testuser@gmail.com", 
        first_name="Jonathan", 
        last_name="Math", 
        description="required", 
        address="334 E 73rd St"
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
            self.token = res.json()["jwt_token"]
        else:
            raise Exception(res.json())
        return res

    def login_user(self, username="newuser", password="password"):
        res = self.post("/user/login/", data={"username": username, "password": password})
        return res
    
class TestRegistration(BaseTestCase):
    
    def test_register_new_user(self):        
        res = self.register_user()
        self.assertTrue(bool(res.json().get("jwt_token")))
        self.assertEqual(res.status_code, 201)
        # # Add assertions to verify that the user was created as expected
        self.assertEqual(Profile.objects.count(), 13)
        res = self.get("/user/me/", auth=True)
        
    
    def test_register_unsuported_block(self):
        data = {
            'username': 'newuser', 
            'password': 'password', 
            'email': 'testuser@gmail.com',
            'first_name': 'Jonathan',
            'last_name': 'Math',
            'description': 'required',
            'address': '34 2nd St',
        }
        res = self.post('/user/register/', data=data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json(), ["Block not supported"])

    def test_register_unknown_block(self):
        data = {
            'username': 'newuser', 
            'password': 'password', 
            'email': 'testuser@gmail.com',
            'first_name': 'Jonathan',
            'last_name': 'Math',
            'description': 'required',
            'address': '34 westndst',
        }
        res = self.post('/user/register/', data=data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json(), ["No results found for the provided address."])

    def test_more_than_3_block_members(self):
        pass

    def test_invalid_username(self):
        self.register_user()
        res = self.register_user()
        self.assertEqual(res.status_code, 400)


class TestAuthentication(BaseTestCase):
    # register a new user
    # test authentication by hitting login endpoint
    # logout
    # test user is no longer authenticated
    def test_good_login(self):
        self.register_user()
        res = self.login_user()
        self.assertEqual(res.status_code, 200)
        
    def test_bad_login(self):
        self.register_user()
        res = self.post("/user/login/", {"username": "newuser", "password": "badpassword"})
        self.assertEqual(res.status_code, 403)
        
        
class TestEditProfile(BaseTestCase):
    # register a new user
    # edit the profile via API endpoint
    # assert that the edit was made
    
    def test_unauth(self):
        res = self.post("/user/edit/", {"first_name": "newname", "last_name": "newlast", "description": "newdesc", "address": "334 Amsterdam Ave W 76th St, New York"})
        self.assertEqual(res.status_code, 403)
    
    def test_user_edit_success(self):
        self.register_user()
        self.login_user()
        res = self.post("/user/edit/", {"username": "backagain","first_name": "newname", "last_name": "newlast", "description": "newdesc", "address": "334 Amsterdam Ave W 76th St, New York"})
    

    def test_sql_injection(self):
        res = self.register_user()
        res = self.login_user()
        res = self.post("/user/edit/", data={"first_name": "newname", "last_name": "newlast", "description": "newdesc", "address": "334 Amsterdam Ave W 76th St, New York; DROP TABLE Profile"})
     
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json(), ["It looks like you might be trying something malicious"])
        
        res = self.post("/user/edit/", data={"first_name": "newname", "email": ";DROP TABLE Profile;", "last_name": "newlast", "description": "newdesc"})

        self.assertEqual(res.status_code, 201)
        
        res = self.get("/user/me/", auth=True)
        self.assertEqual(res.json()["email"], "\\;DROP TABLE Profile\\;")
        
class TestFriendship(BaseTestCase):
    def test_create_friendship(self):
        user_1 = self.register_user(username="newuser1", password="password1")
        user_2 = self.register_user(username="newuser2", email="newuser2@gmail.com", password="password2")
        
        # First user sends a friend request to the second user
        self.login_user(username="newuser1", password="password1")
        res = self.post(f"/friendship/create/{user_2['user_id']}")
        self.assertEqual(res.status_code, 201)
        
        # Second user lists their pending friend requests and accepts the friend request
        self.login_user(username="newuser2", password="password2")
        res = self.get("/friendship/requests/", auth=True)
        self.assertEqual(res.status_code, 200)
        request_id = res.json()[0]["request_id"]
        
        res = self.post(f"/friendship/accept/{request_id}", auth=True)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(len(res.json()), 1)
        friendship_request_id = res.json()[0]
        self.get(f"/friendship/confirm/{friendship_request_id}", auth=True)
        
        # First user checks if they now have one friend
        self.login_user(username="newuser1", password="password1")
        user_info = self.get(f"/user/me/", auth=True).json()
        self.assertEqual(user_info.get('friend_count'), 1)
        self.assertEqual(user_info.get('followers_count'), 0)
        
        # Second user checks if they now have one friend
        self.login_user(username="newuser2", password="password2")
        user_info = self.get(f"/user/me/", auth=True).json()
        self.assertEqual(user_info.get('friend_count'), 1)
        self.assertEqual(user_info.get('followers_count'), 0)

        
class TestThreadCreation(BaseTestCase):

    def test_new_user_thread_non_friend(self):
        res = self.register_user(username="other_user")
        res = self.post("/thread/create/", data={"title": "new thread", "message": "new message", "address": "334 E 73rd Street", "body": "new body", "user_id": 1})
        self.assertEqual(res.status_code, 201)

    def test_new_user_thread_with_friend(self):
        res = self.register_user(username="other_user")
        res = self.post("/thread/create/", data={"title": "new thread", "message": "new message", "address": "334 E 73rd Street", "body": "new body", "user_id": 1})
        res = self.get(f"/thread/{res.json()['thread_id']}/", auth=True)

    def test_new_block_thread(self):
        res = self.register_user(username="other_user")
        res = self.post("/thread/create/", data={"title": "new thread", "message": "new message", "address": "334 E 73rd Street", "body": "new body", "block_id": 1})

        self.assertEqual(res.status_code, 201)
        res = self.get(f"/thread/{res.json()['thread_id']}/", auth=True)
    
    def test_new_hood_thread(self):
        pass

    def test_new_user_thread_msg(self):
        pass
    
    def test_new_block_thread_msg(self):
        pass
    
    def test_new_hood_thread_msg(self):
        pass

    

class TestMessageReply(TestCase):
        
    def test_reply(self):
        pass
    
    def test_reply_not_allowed(self):
        pass
    

class TestSearchFunctionality(TestCase):
    pass

class TestDataVisualizationQueries(TestCase):
    pass
    
class TestBlockConfirmation(TestCase):
    pass

class TestBlockQuery(TestCase):
    pass

class TestHoodQuery(TestCase):
    pass

class TestNotifications(TestCase):
    pass
