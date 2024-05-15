import time

import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission


class JWTAuthentication(BasePermission):

    def authenticate(self, request):
        user = self.authenticate_header(request)
        if not user:
            raise AuthenticationFailed('Unauthenticated')
        return user
    
    def authenticate_header(self, request):
        token = request.headers.get('Authorization')
        if not token:
            return None

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            print("Token EXPIRED")
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            print("Invalid Token")
            raise AuthenticationFailed('Invalid token')

        user_id = payload.get('user_id')
        exp = payload.get('exp')
        if not user_id or not exp or not int(exp) > int(time.time()):
            raise AuthenticationFailed('Invalid token')
        return user_id

    def refresh_token(self, user_id):
        expiration_time = int(time.time()) + settings.JWT_EXPIRATION_TIME
        payload = {'user_id': user_id, 'exp': expiration_time}
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


class LoginRequiredPermission(JWTAuthentication):
    """
    Custom permission class to require login for accessing the view.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated
        user_id = self.authenticate(request)
 
        if user_id:
            request.user = user_id
            return True
        return False
