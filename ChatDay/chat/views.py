from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Message,Topic
from .serializers import MessageSerializer, TopicSerializer
from django.shortcuts import render
import random

class ChatHistoryAPIView(APIView):
    def get(self, request):
        message = Message.objects.all().order_by('-timestamp')
        serializer = MessageSerializer(message, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

class CurrentTopicView(APIView):
    def get(self, request):
        if not Topic.objects.exists(): #사이트 접속시 첫 자정까지 주제 없음 방지 
            topics = ["오늘의 목표는?", "최근 본 영화는?", "가장 좋아하는 음식은?", "티니핑 중에 나는 무슨핑일까"]
            new_topic = random.choice(topics)
            Topic.objects.create(text=new_topic)
        
        topic = Topic.objects.last()  # 가장 최근 주제

        if topic:
            serializer = TopicSerializer(topic)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "현재 주제를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)