from django.http import JsonResponse
from main.auth import LoginRequiredPermission
from main.utils.utils import get_user_id, query_to_json
from rest_framework.views import APIView


# Blocks
class GetBlockThreads(APIView):
    permission_classes = [LoginRequiredPermission]
    
    def get(self, request, block_id):
        sql_query = f"""
            SELECT * FROM Thread t WHERE t.block_id = {block_id};
        """
        return JsonResponse(query_to_json(sql_query))


class GetBlockFollows(APIView):
    permission_classes = [LoginRequiredPermission]
    
    def get(self, request):
        # get blocks that the user follows
        user_id = get_user_id(request)
        sql_query = f"""
            SELECT block_id FROM BlockFollow WHERE user_id = {user_id};
        """
        return JsonResponse(query_to_json(sql_query))

class ListBlockMembers(APIView):
    def get(self, request, block_id):
        sql_query = f"""
            SELECT * FROM Profile p WHERE p.block_id = {block_id} AND p.confirmed=true;
        """
        return JsonResponse(query_to_json(sql_query))