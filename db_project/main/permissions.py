from rest_framework.permission import BasePermission


class LoginRequiredPermission(    def has_permission(self, request, view):
        user = self.authenticate(request)
        if user:
            # Refresh token if necessary
            new_token = self.refresh_token(user)
            request.user = user
            request.auth = new_token
            return True
        return False
)
from rest_framework.permissions import BasePermission
