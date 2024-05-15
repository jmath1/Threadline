from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView

from main.api.general import CustomAPIView
from main.auth import LoginRequiredPermission
from main.utils.utils import (execute, get_cords_from_address, query_to_json,
                              validate_coords)


class GetThread(CustomAPIView):
    permission_classes = [LoginRequiredPermission]
    
    def get(self, request, thread_id):

        sql_query = f"""
           SELECT body, datetime, coords FROM Message WHERE thread_id = {thread_id} ORDER BY datetime; 
        """
    
        data = query_to_json(sql_query)
        if not data:
            data = {}
        else:
            data = data[0]
            
        sql_query = f"""
            SELECT t.title, count(message_id) AS message_count 
            FROM Thread t LEFT JOIN Message m on t.thread_id = m.thread_id 
            WHERE t.thread_id = {thread_id} GROUP BY t.thread_id;
        """
        
        thread = query_to_json(sql_query)
    
        if thread:
            thread = thread[0]
            if thread.get("title"):
                data["title"] = thread["title"]
            if thread.get("message_count"):
                data["message_count"] = thread["message_count"]
        
        return JsonResponse({"results": data})

class GetUserThreads(CustomAPIView):
    permission_classes = [LoginRequiredPermission]
    
    def get(self, request):
        user_id = self.get_user()["user_id"]
        sql_query = f"""
            SELECT t.created, title, p.username AS author_username
            FROM Thread t 
            JOIN Profile p ON t.author_user_id = p.user_id 
            WHERE p.user_id = {user_id} OR author_user_id = {user_id} ORDER BY created DESC;
        """
        data = query_to_json(sql_query)
        
        if request.query_params.get("following") == "true":
            sql_query = f"""
                SELECT t.created, title, p.username AS author_username
                FROM Thread t 
                JOIN Profile p ON t.author_user_id = p.user_id 
                JOIN Friendship f ON f.followee_id = {user_id} 
            """
            follow_data = query_to_json(sql_query)
            if follow_data:
                data = data + follow_data
                data = sorted(data, key=lambda x: x["created"], reverse=True)

        return JsonResponse({"results": data})


class CreateThread(CustomAPIView):
    permission_classes = [LoginRequiredPermission]
    
    def post(self, request):
        
        data = request.data
        error = None
        if not data.get("title"):
            error = "title required"
        if not (data.get("user_id") and not data.get("block_id") and not data.get("hood_id")):
            error = "need thread type" # probably wont hit this unless intentionally trying to throw an error
        if error:
            return JsonResponse(status=400, data={"error": error})
        
        
        user = self.get_user()
        user_id = user["user_id"]
        hood_id = user["hood_id"]
        block_id = user["block_id"]
        
        if request.data.get("threadType") == "UserThread" or request.data.get("user_id"):
            friendship_ids = []
            friendship_ids_sql_query = f"""
                SELECT p.user_id
                FROM Profile p
                JOIN Friendship f ON p.user_id = f.followee_id
                WHERE f.follower_id = {user_id} OR f.followee_id = {user_id} AND f.confirmed=true;
            """
            friendship_ids = query_to_json(friendship_ids_sql_query)
            
        coords = None
        if request.data.get("address"):
            coords = get_cords_from_address(request.data.get("address"))
            valid_coords = validate_coords(coords, user, validity_type=None)
        
        if coords and not valid_coords:
            return JsonResponse(status=400, data={"error": "coords not supported"})
        if data.get("user_id") and data.get("user_id")  not in [k["user_id"] for k in friendship_ids]:
            return JsonResponse(status=403, data={"error": "user_id not a friend"})

        if data.get("hood_id") and data.get("hood_id") != hood_id:
            return JsonResponse(status=403, data={"error": "hood_id not your hood"})
        if data.get("block_id") and data.get("block_id") != block_id:
            return JsonResponse(status=403, data={"error": "block_id not your block"})
        
        sql_query = f"""
            INSERT INTO Thread (user_id, author_user_id, block_id, hood_id, title)
            VALUES ({request.data.get("user_id") if user_id is not None else "NULL"},
                    {user_id}, 
            {request.data.get("block_id") if request.data.get("block_id") else "NULL"},
            {request.data.get("hood_id") if request.data.get("hood_id") else "NULL"},
            '{request.data["title"]}'
    );
            VALUES ({request.data.get("user_id", "NULL")}, {user_id}, {request.data.get("block_id", "NULL")}, {request.data.get("hood_id", "NULL")}, '{request.data["title"]}');
        """
        thread_id = execute(sql_query)

        sql_query = f"""
            INSERT INTO Message(thread_id, user_id, coords, body)
            VALUES ({thread_id},{user_id}, {coords if coords else "NULL"}, '{request.data.get("messageBody")}');
        """
        

        execute(sql_query)
        return HttpResponse(status=201)
    
    
class GetBlockThreads(CustomAPIView):
    permission_classes = [LoginRequiredPermission]
    
    def get(self, request):
        block_id = self.get_user()["block_id"]
        user_id = self.get_user()["user_id"]
        sql_query = f"""
            SELECT t.created, t.title, p.username AS author_username FROM Thread t JOIN Profile p ON t.author_user_id = p.user_id WHERE t.block_id = {block_id} AND t.user_id = {user_id} ORDER BY t.created DESC;
        """
        data = query_to_json(sql_query)
        if request.query_params.get("following") == "true":
            sql_query = f"""
                SELECT t.created, t.thread_id, t.title, p.username AS author_username
                FROM Thread t
                JOIN Profile p ON t.author_user_id = p.user_id
                JOIN Block b ON t.block_id = b.block_id
                JOIN UserFollowBlock fb ON fb.block_id = b.block_id
                WHERE fb.user_id = {user_id};
            """
            follow_data = query_to_json(sql_query)
        
            if follow_data:
                data = data + follow_data
                # doing this to bypass issue of timezones naivity when sorting on created in a query
                data = sorted(data, key=lambda x: x["created"], reverse=True)

        return JsonResponse({"results": data})

class GetHoodThreads(CustomAPIView):
    permission_classes = [LoginRequiredPermission]
    
    def get(self, request):
        user = self.get_user()
        hood_id = user["hood_id"]
        user_id = user["user_id"]
        sql_query = f"""SELECT t.created, t.thread_id, t.title, p.username AS author_username FROM Thread t JOIN Profile p on p.user_id=t.author_user_id WHERE hood_id = {hood_id} ORDER BY t.created DESC"""
        data = query_to_json(sql_query) 
        
        if request.query_params.get("following") == "true":
            sql_query = f"""
                SELECT t.created, t.thread_id, t.title, p.username as author_username
                FROM Thread t
                JOIN Profile p ON t.author_user_id = p.user_id
                JOIN Hood h ON t.hood_id = h.hood_id
                JOIN UserFollowHood fh ON fh.hood_id = h.hood_id
                WHERE fh.user_id = {user_id}
            """
            follow_data = query_to_json(sql_query)

            if follow_data:
                data = follow_data + data
                data = sorted(data, key=lambda x: x["created"], reverse=True)
        return JsonResponse({"results": data})
        
    

class DeleteThread(APIView):
    permission_classes = [LoginRequiredPermission]
    
    def delete(self, request, thread_id):
        sql_query = f"""
            DELETE FROM Thread WHERE thread_id = {thread_id};
        """
        execute(sql_query)
        return JsonResponse(status=204)


class FollowThread(CustomAPIView):
    permission_classes = [LoginRequiredPermission]
    
    def post(self, request, thread_id):
        user_id = self.get_user()["user_id"]
        sql_query = f"""
            INSERT INTO ThreadFollow (user_id, thread_id)
            VALUES ({user_id}, {thread_id})
            RETURNING;
        """
        execute(sql_query)
        return JsonResponse(status=201)

class UnfollowThread(CustomAPIView):
    permission_classes = [LoginRequiredPermission]
    
    def delete(self, request, thread_id):
        user_id = self.get_user()["user_id"]
        sql_query = f"""
            DELETE FROM ThreadFollow WHERE user_id={user_id} AND thread_id={thread_id};
        """
        execute(sql_query)
        return JsonResponse(status=204)

class ListThreadMembers(APIView):
    permission_classes = [LoginRequiredPermission]
    
    def get(self, request, thread_id):
        sql_query = f"""
            SELECT p.username, p.user_id, p.firstname, p.lastname FROM Profile p
            JOIN UserThread ut ON p.user_id = ut.user_id
            WHERE ut.thread_id = {thread_id};
        """
        return JsonResponse(query_to_json(sql_query))

class ListThreadMessages(APIView):
    permission_classes = [LoginRequiredPermission]
    
    def get(self, request, thread_id):
        sql_query = f"""
            SELECT * FROM Message m WHERE m.thread_id = {thread_id};
        """
        return JsonResponse(query_to_json(sql_query))
    
class EditDeleteMessage(APIView):
    permission_classes = [LoginRequiredPermission]
    
    def post(self, request, message_id):
        sql_query = f"""
            UPDATE Message
            SET content = {request.data["content"]}
            WHERE message_id = {message_id};
        """
        execute(sql_query)
        return JsonResponse(status=201)
    
    def delete(self, request, message_id):
        sql_query = f"""
            DELETE FROM Message WHERE message_id = {message_id};
        """
        execute(sql_query)
        return JsonResponse(status=204)

class CreateMessage(APIView):
    permission_classes = [LoginRequiredPermission]
    
    def post(self, request):
        user_id = self.get_user()["user_id"]
        # geocode address to make into coords here
        sql_query = f"""
            INSERT INTO Message (thread_id, user_id, content, coords)
            VALUES ({request.data["thread_id"]}, {user_id}, {request.data["content"]})
            RETURNING;
        """
        execute(sql_query)
        return JsonResponse(status=201)