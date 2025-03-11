import asyncio
import json

import redis
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings

redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = str(self.scope["user"].id)
        if not self.user_id:  # Handle unauthenticated users
            await self.close()
            return
        
        self.channel_name = f"notifications:user:{self.user_id}"
        self.pubsub = redis_client.pubsub()
        self.pubsub.subscribe(self.channel_name)

        await self.accept()

        # Start listening for messages from Redis
        asyncio.create_task(self.listen_for_notifications())

    async def listen_for_notifications(self):
        """Continuously listen for messages from Redis and send them to WebSocket"""
        while True:
            message = self.pubsub.get_message(ignore_subscribe_messages=True)
            if message:
                await self.send(text_data=json.dumps({"notification": message["data"]}))
            await asyncio.sleep(0.1)  # Prevent busy waiting

    async def disconnect(self, close_code):
        self.pubsub.unsubscribe(self.channel_name)
