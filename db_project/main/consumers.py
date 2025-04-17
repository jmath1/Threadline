import json
import redis.asyncio as aioredis
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from asgiref.sync import sync_to_async
import asyncio

REDIS_HOST = settings.REDIS_HOST
REDIS_PORT = settings.REDIS_PORT
REDIS_DB = settings.REDIS_DB

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.pubsub = None
        self.redis = None
        self.hood_group_name = None

        if not self.user.is_authenticated:
            await self.close()
            return

        # Get user's hood
        my_hood = await sync_to_async(lambda: self.user.hood)()
        if not my_hood:
            await self.close()
            return

        self.hood_group_name = f"chat:hood:{my_hood.id}"
        self.redis = await aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}")
        self.pubsub = self.redis.pubsub()
        await self.pubsub.subscribe(self.hood_group_name)

        await self.accept()
        asyncio.create_task(self.listen_for_chats())

    async def disconnect(self, close_code):
        if self.pubsub:
            await self.pubsub.unsubscribe(self.hood_group_name)
        if self.redis:
            await self.redis.close()

    async def listen_for_chats(self):
        while True:
            try:
                message = await self.pubsub.get_message(ignore_subscribe_messages=True, timeout=1)
                if message and message["type"] == "message":
                    await self.send(text_data=json.dumps({"message": message["data"].decode()}))
                await asyncio.sleep(0.1)
            except Exception as e:
                print(f"Error in listen_for_chats: {e}")
                break

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data.get("message")

            if not message:
                return

            my_hood = await sync_to_async(lambda: self.user.hood)()
            pub_data = {
                "user": self.user.email,
                "message": message,
            }
            if not my_hood:
                await self.send(text_data=json.dumps({"error": "Unauthorized: You can only send messages to your own hood"}))
                return

            hood_group_name = f"chat:hood:{my_hood.id}"
            await self.redis.publish(hood_group_name, json.dumps(pub_data))
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({"error": "Invalid JSON"}))
        except Exception as e:
            await self.send(text_data=json.dumps({"error": f"Error processing message: {str(e)}"}))

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
        if self.redis:
            await self.redis.close()

    async def listen_for_notifications(self):
        while True:
            message = await self.pubsub.get_message(ignore_subscribe_messages=True, timeout=1)
            if message and message["type"] == "message":
                await self.send(text_data=json.dumps({"notification": message["data"].decode()}))
            await asyncio.sleep(0.1)