import json
import redis
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message, Topic




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

        await self.save_message(user, message, topic)
        


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
    
async def save_message(self, user, message, topic):
        # 메시지를 데이터베이스에 저장할 때 topic을 추가합니다.
        Message.objects.create(user=user, content=message, topic=topic)