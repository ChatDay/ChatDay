from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Message,Topic
from .serializers import MessageSerializer, TopicSerializer
from django.shortcuts import render

class ChatHistoryAPIView(APIView):
    def get(self, request):
        message = Message.objects.all().order_by('-timestamp')
        serializer = MessageSerializer(message, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

class CurrentTopicView(APIView):
    def get(self, request):
        # 최신 주제 가져오기
        topic = Topic.objects.last()  # 가장 최근 주제
        if topic:
            serializer = TopicSerializer(topic)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "현재 주제를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)