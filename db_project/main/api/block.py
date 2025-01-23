from django.http import JsonResponse
from rest_framework.views import APIView


# Blocks
class GetBlockThreads(APIView):
    permission_classes = []
    
    def get(self, request, block_id):
        sql_query = f"""
            SELECT * FROM Thread t WHERE t.block_id = {block_id};
        """
        return JsonResponse(query_to_json(sql_query))


class GetBlockFollows(APIView):
    permission_classes = []
    
    def get(self, request):
        # get blocks that the user follows
        user_id = None
        if request.user.is_authenticated:
            
            user_id = request.user
            
        if not user_id:
            return JsonResponse({"error": "User not found"}, status=404)
        else:
            return request.user.objects.get_followed_blocks(user_id)

class ListBlockMembers(APIView):
    def get(self, request, block_id):
        sql_query = f"""
            SELECT * FROM User p WHERE p.block_id = {block_id} AND p.confirmed=true;
        """
        return JsonResponse(query_to_json(sql_query))