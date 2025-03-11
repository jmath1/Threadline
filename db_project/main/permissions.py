from django.shortcuts import get_object_or_404
from main.models import Thread
from rest_framework.permissions import BasePermission


class ThreadPermission(BasePermission):
    """
    Only allow if the user is tagged or if the user is in the thread's hood.
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
    Only allow if the user is tagged or if the user is in the thread's hood.
    """
    def has_permission(self, request, view):
        if request.method == "POST":
            thread_id = request.data.get("thread_id")
            thread = get_object_or_404(Thread, id=thread_id)
            # users can only create messages in their hood threads, that they are tagged in
            if thread:
                return thread.hood == request.user.hood or request.user in thread.participants.all()
        elif request.method == "GET":
            obj = view.get_object()
            # users can only see hood threads or threads that they are tagged in
            if obj.thread.hood:
                return True
            if obj.user == request.user:
                return True
        elif request.method in ["DELETE", "PUT"]:
            obj = view.get_object()
            # users can only delete their own threads
            return obj.author_id == request.user.id
        return False
