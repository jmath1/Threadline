from django.test import Client, TestCase
from unittest.mock import patch, MagicMock
from main.models import Profile

def mock_requests_get(json_data, status_code=200):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Setup the mock to return a custom response
            mock_response = MagicMock()
            mock_response.json.return_value = json_data
            mock_response.status_code = status_code
            
            with patch('requests.get', return_value=mock_response) as mock_get:
                return func(*args, **kwargs, mock_get=mock_get)
        return wrapper
    return decorator

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
    
    @mock_requests_get({'longt': '-73.95420','latt': '40.76774'})
    def test_register_new_user(self, mock_get):        
        # happy path
        res = self.register_user()
        self.assertTrue(self.client.cookies.get('jwt_token'))
        self.assertEqual(res.status_code, 201)
        # # Add assertions to verify that the user was created as expected
        self.assertEqual(Profile.objects.count(), 13)
        user = Profile.objects.get(username='newuser')
        # check confirmation
        self.assertEqual(user[-1], True)
    
    @mock_requests_get({'longt': '-73.96979','latt': '40.75314'}) #unsported block 
    def test_register_unsuported_block(self, mock_get):
        data = {
            'username': 'newuser', 
            'password': 'password', 
            'email': 'testuser@gmail.com',
            'first_name': 'Jonathan',
            'last_name': 'Math',
            'description': 'required',
            'address': '34 2nd St',
        }
        res = self.client.post('/user/register/', data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json(), ["Block not supported"])

    @mock_requests_get({'error': {'description': 'Your request produced no suggestions.', 'code': '018'}})
    def test_register_unknown_block(self, mock_get):
        data = {
            'username': 'newuser', 
            'password': 'password', 
            'email': 'testuser@gmail.com',
            'first_name': 'Jonathan',
            'last_name': 'Math',
            'description': 'required',
            'address': '34 westndst',
        }
        res = self.client.post('/user/register/', data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json(), ["No results found for the provided address."])

    @mock_requests_get({'longt': '-73.95420','latt': '40.76774'})
    def test_more_than_3_block_members(self, mock_get):
        pass

    @mock_requests_get({'longt': '-73.95420','latt': '40.76774'})
    def test_invalid_username(self, mock_get):
        self.register_user()
        res = self.register_user()
        self.assertEqual(res.status_code, 400)


class TestAuthentication(BaseTestCase):
    # register a new user
    # test authentication by hitting login endpoint
    # logout
    # test user is no longer authenticated
    @mock_requests_get({'longt': '-73.95420','latt': '40.76774'})
    def test_good_login(self, mock_get):
        self.register_user()
        res = self.login_user()
        self.assertEqual(res.status_code, 200)
        
    @mock_requests_get({'longt': '-73.95420','latt': '40.76774'})
    def test_bad_login(self, mock_get):
        self.register_user()
        res = self.client.post("/user/login/", {"username": "newuser", "password": "badpassword"})
        self.assertEqual(res.status_code, 403)
        
        
class TestEditProfile(BaseTestCase):
    # register a new user
    # edit the profile via API endpoint
    # assert that the edit was made
    
    def test_unauth(self):
        
        res = self.client.post("/user/edit/", {"first_name": "newname", "last_name": "newlast", "description": "newdesc", "address": "334 Amsterdam Ave W 76th St, New York"})
        self.assertEqual(res.status_code, 403)
    
    @mock_requests_get({'longt': '-73.95420','latt': '40.76774'})
    def test_user_edit_success(self, mock_get):
        self.register_user()
        self.login_user()
        res = self.client.post("/user/edit/", {"username": "backagain","first_name": "newname", "last_name": "newlast", "description": "newdesc", "address": "334 Amsterdam Ave W 76th St, New York"})
    

    def test_sql_injection(self):
        res = self.register_user()
        res = self.login_user()
        res = self.client.post("/user/edit/", {"first_name": "newname", "last_name": "newlast", "description": "newdesc", "address": "334 Amsterdam Ave W 76th St, New York; DROP TABLE Profile"})
     
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json(), ["It looks like you might be trying something malicious"])
        
        res = self.client.post("/user/edit/", {"first_name": "newname", "email": ";DROP TABLE Profile;", "last_name": "newlast", "description": "newdesc"})

        self.assertEqual(res.status_code, 201)
        
        res = self.client.get("/user/me/")
        self.assertEqual(res.json()["email"], "\\;DROP TABLE Profile\\;")

class TestThreadCreation(TestCase):
    # create a new usag
    def test_new_user_thread(self):
        pass
    
    def test_new_block_thread(self):
        pass
    
    def test_new_hood_thread(self):
        pass

class TestMessagePosting(TestCase):
    # create a new usag
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
