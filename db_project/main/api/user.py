from django.db import transaction
from django.db.models import Q
from django.db.utils import IntegrityError
from drf_yasg.utils import swagger_auto_schema
from main.models import User
from main.serializers.user import (EditUserSerializer, MeSerializer,
                                   UserSerializer)
from main.utils.utils import process_coords
from rest_framework import status
from rest_framework.generics import (CreateAPIView, GenericAPIView,
                                     RetrieveAPIView)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class GetUserDetail(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
    def get_object(self):
        return self.get_queryset().get(user_id=self.kwargs["pk"]).annotate("followers_count", "following_count", "friends_count")
    
    @swagger_auto_schema(
        operation_description="Get user details",
        responses={200: UserSerializer},
    )
    def get(self, request, pk):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    

class UserRegisterView(CreateAPIView):
    """
    Endpoint to register a new user.
    """
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    
    @swagger_auto_schema(
        operation_description="Register a new user",
        responses={201: "User registered successfully"},
    )
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


class MeGET(GenericAPIView):
    serializer_class = MeSerializer
    
    def get(self, request):
        """
        Get the authenticated user's details
        """
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data)

class EditUserView(GenericAPIView):
    
    serializer_class = EditUserSerializer

    def post(self, request):
        """
        Edit user details
        """
        user = request.user
        serializer = self.serializer_class(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(user, serializer.validated_data)
        return Response(serializer.data)

