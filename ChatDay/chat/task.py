from celery import shared_task
from .models import Message, Topic
import random
import redis

# Redis 연결 설정
redis_client = redis.StrictRedis(host='redis', port=6379, db=0, decode_responses=True)

@shared_task
def clear_chat_and_update_topic():
    # 1. 채팅 기록 삭제
    Message.objects.all().delete()
    
    # 2. 새로운 주제 설정
    topics = ["오늘의 목표는?", "최근 본 영화는?", "가장 좋아하는 음식은?", "티니핑 중에 나는 무슨핑일까"]
    new_topic = random.choice(topics)
    
    # 새로운 주제 추가
    Topic.objects.create(text=new_topic)
    
    print(f"새로운 주제 '{new_topic}'가 추가되고 채팅 기록이 삭제되었습니다.")

@shared_task
def save_messages_to_db():  # Redis에서 채팅 메시지를 가져와 DB에 저장
    # Redis 스트림에서 메시지 가져오기
    messages = redis_client.xrange('chat_room')  # chat_room은 채팅방 스트림 이름

    if not messages:
        print("No messages to save.")
        return  # 메시지가 없으면 함수 종료

    for message_id, message_data in messages:
        # Redis에서 메시지 가져와 DB에 저장
        Message.objects.create(user=message_data['user'], content=message_data['message'], topic=message_data['topic'])
        redis_client.xdel('chat_chat_room', message_id)