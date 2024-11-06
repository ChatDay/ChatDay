from celery import shared_task
from .models import Message, Topic
import random

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