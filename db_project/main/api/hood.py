from django.http import JsonResponse
from rest_framework.views import APIView


class GetHoodFollows(APIView):
    permission_classes = []
    
    def get(self, request):
        # get hoods that the user follows
        if request.user.is_authenticated:
            hood_follows = request.user.hood_follow.all()
            return JsonResponse({"results": [hood.serialize() for hood in hood_follows]})
        else:
            return JsonResponse({"error": "User not found"}, status=403)
            
    

class ListHoodMembers(APIView):
    permission_classes = []
    
    def get(self, request, hood_id):
        self.get_user()
        sql_query = f"""
            SELECT * FROM User p 
            JOIN Block b ON b.block_id = p.block_id 
            WHERE p.hood_id = {hood_id};
        """
        return JsonResponse(query_to_json(sql_query))

