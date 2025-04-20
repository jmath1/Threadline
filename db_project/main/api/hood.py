from drf_yasg.utils import swagger_auto_schema
from main.models import Hood, User
from main.serializers.follow import FollowerUserSerializer
from main.serializers.hood import HoodSerializer
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

class ListHoods(ListAPIView):
    """
    Endpoint to list all hoods.
    """
    serializer_class = HoodSerializer
    queryset = Hood.objects.all()
    
    @swagger_auto_schema(
        operation_description="Get all hoods",
        responses={200: HoodSerializer},
    )
    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
class GetUserHoodsFollowed(ListAPIView):
    serializer_class = HoodSerializer
    
    def get_queryset(self):
        return self.request.user.get_hoods_followed()

    @swagger_auto_schema(
        operation_description="Get hoods that the user follows",
        responses={200: HoodSerializer},
    )
    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
class GetHoodFollowers(ListAPIView):
    serializer_class = FollowerUserSerializer
    
    def get_queryset(self):
        if not self.kwargs.get("pk"):
            return Hood.objects.none()
        return Hood.objects.get(pk=self.kwargs["pk"]).followers.all()
    
    @swagger_auto_schema(
        operation_description="Get followers of a hood",
        responses={200: FollowerUserSerializer},
    )
    def get(self, request, hood_id):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

class ListHoodMembers(ListAPIView):
    serializer_class = FollowerUserSerializer
    
    def get_queryset(self):
        if not self.kwargs.get("pk"):
            return User.objects.none()
        return User.objects.filter(hood=self.kwargs["pk"])
    
    @swagger_auto_schema(
        operation_description="Get members of a hood",
        responses={200: FollowerUserSerializer},
    )
    def get(self, request, hood_id):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
