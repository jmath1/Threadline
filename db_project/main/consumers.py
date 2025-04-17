import json
import redis.asyncio as aioredis
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
from django.conf import settings

REDIS_HOST = settings.REDIS_HOST
REDIS_PORT = settings.REDIS_PORT
REDIS_DB = settings.REDIS_DB

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.pubsub = None
        

        self.group_name = f"chat:{self.user.id}"
        self.redis = await aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}")
        
        self.pubsub = self.redis.pubsub()
        await self.pubsub.subscribe(self.group_name)

        await self.accept()
        print("Accepted! Listening now")
        asyncio.create_task(self.listen_for_chats())


    async def disconnect(self, close_code):
        if self.pubsub:
            await self.pubsub.unsubscribe(self.group_name)
            await self.redis.close()

    async def listen_for_chats(self):
        my_hood = self.scope["user"].hood
        if my_hood:
            hood_group_name = f"chat:hood:{my_hood.id}"
            await self.pubsub.subscribe(hood_group_name)
            while True:
                message = await self.pubsub.get_message(ignore_subscribe_messages=True, timeout=1)
                if message and message["type"] == "message":
                    await self.send(text_data=json.dumps({"message": message["data"].decode()}))
                await asyncio.sleep(0.1)
                
class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.pubsub = None

        self.group_name = f"notifications:{self.user.id}"
        self.redis = await aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}")

        self.pubsub = self.redis.pubsub()
        await self.pubsub.subscribe(self.group_name)

        await self.accept()
        print("Accepted! Listening now")
        asyncio.create_task(self.listen_for_notifications())

    async def disconnect(self, close_code):
        if self.pubsub:
            await self.pubsub.unsubscribe(self.group_name)
            await self.redis.close()

    async def listen_for_notifications(self):
        while True:
            message = await self.pubsub.get_message(ignore_subscribe_messages=True, timeout=1)
            if message and message["type"] == "message":
                await self.send(text_data=json.dumps({"notification": message["data"].decode()}))
            await asyncio.sleep(0.1)