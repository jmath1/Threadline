
from django.contrib.gis.geos import Point
from django.test import TestCase
from main.tests.base import BaseTestCase

class TestThreadCreation(BaseTestCase):

    def test_new_user_thread_non_friend(self):
        # self.mock_geocode_address.return_value = Point(-75.1764407, 39.9404423, srid=4326)
        # res = self.register_user(username="other_user")
        # res = self.post("/thread/create/", data={"title": "new thread", "message": "new message", "address": "334 E 73rd Street", "body": "new body", "user_id": 1})
        # self.assertEqual(res.status_code, 201)
        pass

    def test_new_user_thread_with_friend(self):
        # self.mock_geocode_address.return_value = Point(-75.1764407, 39.9404423, srid=4326)
        # res = self.register_user(username="other_user")
    # res = self.post("/thread/create/", data={"title": "new thread", "message": "new message", "address": "334 E 73rd Street", "body": "new body", "user_id": 1})
        # res = self.get(f"/thread/{res.json()['thread_id']}/", auth=True)
        pass
    
    
    def test_new_hood_thread(self):
        pass

    def test_new_user_thread_msg(self):
        pass
    
    # def test_new_block_thread_msg(self):
    #     pass
    
    def test_new_hood_thread_msg(self):
        pass

    

class TestMessageReply(TestCase):
        
    def test_reply(self):
        pass
    
    def test_reply_not_allowed(self):
        pass