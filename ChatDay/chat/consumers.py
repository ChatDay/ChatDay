import json
import redis
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, Topic

redis_client = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "room"
        self.room_group_name = "chat_%s" % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = text_data_json['user']
        topic =Topic.objects.last()

        await self.save_message_to_redis(user, message, topic.text) #토픽 모델 안에 있는 text만 선택


        await self.channel_layer.group_send(
            self.room_group_name,
        {
            'type' : 'chat_message',
            'message' : message,
            'user' : user,
        }
    )
    
    async def chat_message(self, event):
        message = event['message']
        user = event['user']

        await self.send(text_data=json.dumps({
            'message' : message,
            'user' : user,
        }))
    

    async def save_message_to_redis(self, user, message, topic):
        redis_client.xadd(self.room_group_name, {
        'user': user,
        'message': message,
        'topic': topic
        })