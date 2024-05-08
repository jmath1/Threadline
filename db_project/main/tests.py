from django.test import Client, TestCase

from main.models import Profile


class BaseTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        
    def register_user(self):
        data = {
            'username': 'newuser', 
            'password': 'password', 
            'email': 'testuser@gmail.com',
            'first_name': 'Jonathan',
            'last_name': 'Math',
            'description': 'required',
            'address': '334 E 73rd St',
        }
        res = self.client.post('/user/register/', data)
        return res

    def login_user(self):
        res = self.client.post("/user/login/", {"username": "newuser", "password": "password"})
        return res
class TestRegistration(BaseTestCase):
            
    def test_register_new_user(self):
        # happy path
        res = self.register_user()
        self.assertEqual(res.status_code, 201)
        # # Add assertions to verify that the user was created as expected
        self.assertEqual(Profile.objects.count(), 13)
        user = Profile.objects.get(username='newuser')
        # check confirmation
        self.assertEqual(user[-1], True)
        
    def test_more_than_3_block_members(self):
        pass

    def test_invalid_address(self):
        pass
    
    def test_invalid_username(self):
        pass
        


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
        res = self.client.post("/user/login/", {"username": "newuser", "password": "badpassword"})
        self.assertEqual(res.status_code, 403)
        
        
class TestEditProfile(BaseTestCase):
    # register a new user
    # edit the profile via API endpoint
    # assert that the edit was made
    
    def test_unauth(self):
        self.register_user()
        
        res = self.client.post("/user/edit/", {"first_name": "newname", "last_name": "newlast", "description": "newdesc", "address": "334 Amsterdam Ave W 76th St, New York"})
        self.assertEqual(res.status_code, 403)
        
    def test_user_edit_success(self):
        self.register_user()
        self.login_user()
        res = self.client.post("/user/edit/", {"username": "backagain","first_name": "newname", "last_name": "newlast", "description": "newdesc", "address": "334 Amsterdam Ave W 76th St, New York"})
    
    def test_sql_injection(self):
        res = self.register_user()
        res = self.login_user()
        res = self.client.post("/user/edit/", {"first_name": "newname", "last_name": "newlast", "description": "newdesc", "address": "334 Amsterdam Ave W 76th St, New York; DROP TABLE Profile"})
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json(), ["There was a problem with the given address"])
        
        res = self.client.post("/user/edit/", {"first_name": "newname", "email": ";DROP TABLE Profile;", "last_name": "newlast", "description": "newdesc"})

        self.assertEqual(res.status_code, 201)
        
        res = self.client.get("/user/me/")
        self.assertEqual(res.json()["email"], "\\;DROP TABLE Profile\\;")
        
class TestMessagePosting(TestCase):
    # create a new usag
    pass 

class TestMessageReply(TestCase):
    pass

class TestThreadCreation(TestCase):
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
