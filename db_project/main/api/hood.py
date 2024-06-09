from django.http import JsonResponse
from main.api.general import CustomAPIView
from main.auth import LoginRequiredPermission
from main.utils.utils import get_user_id, query_to_json
from rest_framework.views import APIView


class GetHoodFollows(APIView):
    permission_classes = [LoginRequiredPermission]
    
    def get(self, request):
        # get hoods that the user follows
        user_id = get_user_id(request)
        sql_query = f"""
            SELECT hood_id FROM HoodFollow WHERE user_id = {user_id};
        """
        return JsonResponse(query_to_json(sql_query))
    

class ListHoodMembers(CustomAPIView):
    permission_classes = [LoginRequiredPermission]
    
    def get(self, request, hood_id):
        self.get_user()
        sql_query = f"""
            SELECT * FROM Profile p 
            JOIN Block b ON b.block_id = p.block_id 
            WHERE p.hood_id = {hood_id};
        """
        return JsonResponse(query_to_json(sql_query))

