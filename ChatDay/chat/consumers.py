import json
import redis
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, Topic

redis_client = redis.StrictRedis(host='redis', port=6379, db=1, decode_responses=True)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "chat_room"
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
        topic_id=1

        if not topic_id:
            print("Topic ID is missing!")  # 디버깅용 로그
            return

        # topic 객체 가져오기
        try:
            topic = Topic.objects.get(id=topic_id)
        except Topic.DoesNotExist:
            print(f"Topic with ID {topic_id} does not exist.")
            return

        await self.save_message_to_redis(user, message, topic)
        


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
    # Redis Streams를 사용하여 메시지 추가
        redis_client.xadd(self.room_group_name, {
        'user': str(user),  # user도 객체라면 문자열로 변환 필요
        'message': message,
        'topic': str(topic)  # topic 객체를 문자열로 변환
        })