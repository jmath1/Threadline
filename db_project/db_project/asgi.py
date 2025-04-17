"""
ASGI config for db_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.layers import get_channel_layer
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import re_path
from main.consumers import ChatConsumer, NotificationConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "db_project.settings")


application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # HTTP request handling (normal Django views)
    "websocket": AuthMiddlewareStack(  # WebSocket connection handling
        URLRouter([
            re_path(r'ws/chat/$', ChatConsumer.as_asgi()),  # Remove trailing slash
            #re_path(r'ws/notifications/$', NotificationConsumer.as_asgi()),  # WebSocket URL for notifications
        ])
    ),
})