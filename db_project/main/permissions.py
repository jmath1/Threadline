from rest_framework.permissions import BasePermission


class ThreadPermission(BasePermission):
    """
    Custom permission to only allow if the user is tagged or if the user is in the thread's hood.
    """
    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            # users can only see hood threads or threads that they are tagged in
            if obj.hood == request.user.hood:
                return True
            if request.user in obj.participants.all():
                return True
            if obj.type == "PUBLIC":
                return True
            
        if request.method == "DELETE":
            # users can only delete the threads they started
            return obj.author == request.user
        if request.method == "POST":
            # users can only create threads in their own hoods
            if obj.hood:
                return obj.hood == request.user.hood
            else:
                return True            
        return False
        
class MessagePermission(BasePermission):
    """
    Custom permission to only allow if the user is tagged or if the user is in the thread's hood.
    """
    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            # users can only see hood threads or threads that they are tagged in
            if obj.thread.hood:
                return True
            if obj.user == request.user:
                return True
        if request.method in ["DELETE", "PUT"]:
            # users can only delete their own threads
            return obj.author == request.user
        if view.action == "create":
            return obj.thread.hood == request.user.hood or request.user in obj.thread.participants.all()
        return False
