from django.http import HttpResponse, JsonResponse


from rest_framework.generics import GenericAPIView
from main.models import Thread, Message
from django.db.models import Count
from django.db.models import Q

class GetThread(GenericAPIView):
    permission_classes = []
    
    def get(self, request, thread_id):

        messages = Message.objects.filter(thread_id=thread_id).values("message_id", "body", "datetime", "coords")
        
        thread = Thread.objects.get(thread_id=thread_id).annotate(message_count=Count("message_id"))
        
        
        print(messages)
        return JsonResponse({"results": {"thread": thread, "messages": messages}})

class GetUserThreads(GenericAPIView):
    def get_queryset(self, request):
        return Thread.objects.filter(Q(user_id=request.user) | Q(author_user_id=request.user))


class CreateThread(GenericAPIView):
    
    def post(self, request):
        data = request.data
        error = None

        if not data.get("title"):
            error = "title required"
        if not data.get("messageBody"):
            error = "message required"
        if (not data.get("user_id") and not data.get("block_id") and not data.get("hood_id")):
            error = "need thread type" # probably wont hit this unless intentionally trying to throw an error
        if error:
            print(data)
            print(error)
            return JsonResponse(status=400, data={"error": error})
        
        
        user = self.get_user()
        user_id = user["user_id"]
        hood_id = data.get("hood_id")
        block_id = data.get("block_id")
        # can only send a UserThread to friends, so we check friendships
        if request.data.get("threadType") == "UserThread" or request.data.get("user_id"):
            friendship_ids = []
            friendship_ids_sql_query = f"""
                SELECT p.user_id
                FROM User p
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
        if data.get("user_id") and data.get("user_id")  not in [str(k["user_id"]) for k in friendship_ids]:
            return JsonResponse(status=403, data={"error": "user_id not a friend"})

        if data.get("hood_id") and data.get("hood_id") != user["hood_id"]:
            return JsonResponse(status=403, data={"error": "hood_id not your hood"})
        if data.get("block_id") and data.get("block_id") != user["block_id"]:
            return JsonResponse(status=403, data={"error": "block_id not your block"})
        # insert the thread
        sql_query = """
            INSERT INTO Thread (user_id, author_user_id, block_id, hood_id, title)
            VALUES (%s, %s, %s, %s, %s) RETURNING thread_id;
        """
        params = (data.get("user_id" if data.get("user_id") else None), user_id if user_id != '' else None, block_id, hood_id, data.get("title"))
        thread_id = execute(sql_query, params=params, fetch=True)
        if thread_id:
            thread_id = thread_id[0] 

        if coords:
            # Including the geometry function directly in the SQL command if coordinates are provided
            sql_query = """
                INSERT INTO Message (thread_id, user_id, body, coords)
                VALUES (%s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326));
            """
            params = (thread_id, user_id, data.get("messageBody"), coords[0], coords[1])
        else:
            # No coordinates provided, handle as NULL
            sql_query = """
                INSERT INTO Message (thread_id, user_id, body, coords)
                VALUES (%s, %s, %s, NULL);
            """
            params = (thread_id, user_id, data.get("messageBody"))
        thread_id = execute(sql_query, params=params)
        return HttpResponse(status=201)
    
    
# class GetBlockThreads(GenericAPIView):
    
#     def get(self, request):
#         block_id = self.get_user()["block_id"]
#         user_id = self.get_user()["user_id"]
#         sql_query = f"""
#             SELECT t.thread_id, t.datetime AS created, t.title, p.username AS author_username FROM Thread t JOIN User p ON t.author_user_id = p.user_id WHERE t.block_id = {block_id} AND t.user_id = {user_id} ORDER BY t.datetime DESC;
#         """
#         data = query_to_json(sql_query)
#         if request.query_params.get("following") == "true":
#             sql_query = f"""
#                 SELECT t.datetime, t.thread_id, t.title, p.username AS author_username
#                 FROM Thread t
#                 JOIN User p ON t.author_user_id = p.user_id
#                 JOIN Block b ON t.block_id = b.block_id
#                 JOIN UserFollowBlock fb ON fb.block_id = b.block_id
#                 WHERE fb.user_id = {user_id};
#             """
#             follow_data = query_to_json(sql_query)
        
#             if follow_data:
#                 data = data + follow_data
#                 # doing this to bypass issue of timezones naivity when sorting on created in a query
#                 data = sorted(data, key=lambda x: x["created"], reverse=True)

#         return JsonResponse({"results": data})

class GetHoodThreads(GenericAPIView):
    
    def get(self, request):
        user = self.get_user()
        hood_id = user["hood_id"]
        user_id = user["user_id"]

        if request.query_params.get("following") == "true":
            
            data = Thread.objects.filter(Q(hood_id=hood_id) | Q(hood_folow=request.user)).values("thread_id", "datetime", "title", "author_user_id").sort('created')

        else:
            data = Thread.objects.filter(hood_id=hood_id).values("thread_id", "datetime", "title", "author_user_id").sort('created')
        return JsonResponse({"results": data})
        
    

class DeleteThread(GenericAPIView):
    
    def get_queryset(self, request):
        return Thread.objects.filter(request.user)


# class FollowThread(GenericAPIView):
    
#     def post(self, request, thread_id):
#         user_id = self.get_user()["user_id"]
#         sql_query = f"""
#             INSERT INTO ThreadFollow (user_id, thread_id)
#             VALUES ({user_id}, {thread_id})
#             RETURNING;
#         """
#         execute(sql_query)
#         return JsonResponse(status=201)

# class UnfollowThread(GenericAPIView):
    
#     def delete(self, request, thread_id):
#         user_id = self.get_user()["user_id"]
#         sql_query = f"""
#             DELETE FROM ThreadFollow WHERE user_id={user_id} AND thread_id={thread_id};
#         """
#         execute(sql_query)
#         return JsonResponse(status=204)

# class ListThreadMembers(GenericAPIView):
    
#     def get(self, request, thread_id):
#         sql_query = f"""
#             SELECT p.username, p.user_id, p.firstname, p.lastname FROM User p
#             JOIN UserThread ut ON p.user_id = ut.user_id
#             WHERE ut.thread_id = {thread_id};
#         """
#         return JsonResponse(query_to_json(sql_query))

# class ListThreadMessages(GenericAPIView):
    
#     def get(self, request, thread_id):
#         sql_query = f"""
#             SELECT * FROM Message m JOIN User p ON m.user_id = p.user_id WHERE m.thread_id = {thread_id};
#         """
#         return JsonResponse(query_to_json(sql_query))
    
# class EditDeleteMessage(GenericAPIView):
    
#     def post(self, request, message_id):
#         sql_query = f"""
#             UPDATE Message
#             SET content = {request.data["content"]}
#             WHERE message_id = {message_id};
#         """
#         execute(sql_query)
#         return JsonResponse(status=201)
    
#     def delete(self, request, message_id):
#         sql_query = f"""
#             DELETE FROM Message WHERE message_id = {message_id};
#         """
#         execute(sql_query)
#         return JsonResponse(status=204)


# class DeleteMessage(GenericAPIView):
    
#     def delete(self, request, message_id):
#         sql_query = f"""
#             DELETE FROM Message WHERE message_id = {message_id};
#         """
#         execute(sql_query)
#         return JsonResponse(status=204, data={"message": "Message deleted successfully."})

# class CreateMessage(GenericAPIView):
    
#     def post(self, request, thread_id):
#         user = self.get_user()
#         user_id = user["user_id"]
#         user_block = user["block_id"]
#         user_hood = user["block_id"]
#         address = request.data.get("address")
#         sql_query = "SELECT block_id, hood_id, user_id, author_user_id FROM Thread WHERE thread_id = %s;"        
#         params = (thread_id,)

#         data = execute(sql_query, params=params, fetch=True)
#         if data:
#             thread_block = data[0][0]
#             thread_hood = data[0][1]
#             thread_user = data[0][2]
#             thread_author = data[0][3]
#         else:
#             return JsonResponse({"error": "Sorry,thread does not exist."}, status=404)

        
#         # # Check user permission
#         # if (thread_block and user_block != thread_block) or (thread_hood and user_hood != thread_hood) \
#         #     or ((thread_user and user_id != thread_user) and (user_id != thread_author)):
#         #         return JsonResponse({"error": "Sorry, no write access allowed."}, status=403)

#         # geocode the address
#         if address:
#             longitude, latitude = get_cords_from_address(address)
     
#         sql_query = "INSERT INTO Message (thread_id, user_id, body, coords) VALUES (%s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326));"
#         params = (thread_id,user_id, request.data["body"], longitude, latitude)
#         execute(sql_query, params=params)
#         return JsonResponse(status=201, data={"message": "Message created successfully."}) 
        

# class ThreadSearchView(GenericAPIView):

#     def get(self, request, *args, **kwargs):
#         query = request.GET.get('q', '')

#         if query:
#             # Use raw SQL to filter threads
#             sql_query = sql_query = f"""
#                 SELECT * FROM Thread t JOIN User p ON t.author_user_id = p.user_id
#                 WHERE title ILIKE '%{query}%'
#                 AND (t.user_id IS NULL OR t.author_user_id = {self.get_user()['user_id']} OR t.user_id = {self.get_user()['user_id']})
#                 """

#             data = query_to_json(sql_query)
            
#         else:
#             data = []

#         return JsonResponse(status=200, data={'results': data})