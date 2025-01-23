from django.http import JsonResponse
from main.serializers.user import (EditUserSerializer,
                              UserSerializer)

from main.models import Friendship, User

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from main.models import Friendship
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db.utils import IntegrityError
from main.utils.utils import process_coords
from django.db import transaction
    
class GetUserDetail(APIView):
    
    def get(self, request, user_id):
        data = User.objects.filter(user_id=user_id).values("username", "first_name", "last_name", "email", "block__name", "block__hood__name")
        followers_count = Friendship.objects.filter(followee_id=user_id, confirmed=False).count()
        following_count = Friendship.objects.filter(follower_id=user_id, confirmed=False).count()
        friends_count = Friendship.objects.filter(Q(follower_id=user_id) | Q(followee_id=user_id), confirmed=True).count()
        data[0]["followers_count"] = followers_count
        data[0]["following_count"] = following_count
        data[0]["friends_count"] = friends_count
        
        if data:
            return JsonResponse({"results": data})
        return JsonResponse({}, status=404)
    

class UserRegisterView(APIView):
    """
    Endpoint to register a new user.
    """
    permission_classes = []
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        hood, coords = process_coords(validated_data['address'])

        try:
            user = User(
                username=validated_data['username'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                email=validated_data['email'],
                description=validated_data['description'],
                photo_url=validated_data.get('photo_url', None),
                address=validated_data['address'],
                coords=coords,
                hood=hood,
            )

            user.set_password(validated_data['password'])
            user.save()
        except IntegrityError:
            return Response(
                {"error": "User already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        user.location_confirmed = user.confirm_location(hood)

        token_serializer = TokenObtainPairSerializer(data={
            "username": user.username,
            "password": validated_data['password']
        })

        token_serializer.is_valid(raise_exception=True)
        tokens = token_serializer.validated_data
        return Response(
            {
                "message": "User registered successfully",
                "user_id": user.id,
                "tokens": tokens,
            },
            status=status.HTTP_201_CREATED,
        )

        

class MeGET(APIView):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            try:
                user = User.objects.select_related('hood').get(id=user.id)
                data = {
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "hood_name": user.hood.name if user.hood else None,
                    "description": user.description,
                    "photo_url": user.photo_url,
                    "address": user.address,
                    "coords": f"({user.coords.x} {user.coords.y})" if user.coords else None,
                    "friends_count": user.friends_count,  # Access the computed property
                    "followers_count": user.followers_count,
                    "following_count": user.following_count,
                }
                return JsonResponse(data)
            except User.DoesNotExist:
                return JsonResponse({"error": "User user not found"}, status=404)
        else:
            return JsonResponse({"error": "User not authenticated"}, status=403)

class EditUserView(APIView):

    def save(self, user, **kwargs):
        parameters = {}
        set_clauses = []

        for field, value in kwargs.items():
            if value is not None:
                # Format geographic data specifically
                if field == "coords":
                    # Assuming the input for 'coords' is like '(x, y)'
                    parameters[field] = f"{value}', 4326)"
                    set_clauses.append(f"{field}=ST_PointFromText('POINT{value}', 4326)")
                else:
                    if value != 'NULL':
                        set_clauses.append("{field}='{value}'".format(
                            field=field,
                            value=value
                        ))
                    else:
                        set_clauses.append("{field}={value}".format(
                            field=field,
                            value=value
                        ))

 
        user = User.objects.filter(id=user.id).update(**parameters)

        return user

    def post(self, request):
        serializer = EditUserSerializer(data=request.data)

        if serializer.is_valid():
            self.save(request.user, **serializer.data)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetNeighborList(APIView):
    
    def get(self, request):
        user = request.user
        user_id = user['user_id']
        block_id = user['block_id']
        hood_id = user['hood_id']


        friendships = Friendship.objects.filter(Q(follower_id=user_id) | Q(followee_id=user_id), confirmed=True)
        following = Friendship.objects.filter(follower_id=user_id, confirmed=False)
        block_neighbors = User.objects.filter(block_id=block_id).exclude(user_id=user_id)
        hood_neighbors = User.objects.filter(block__hood_id=hood_id).exclude(user_id=user_id)
        
        results = {
            "block_neighbors": block_neighbors,
            "hood_neighbors": hood_neighbors,
            "friendships_list": friendships,
            "following_list": following
        }

        return JsonResponse(results)


