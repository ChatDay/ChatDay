from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Message
from .serializers import MessageSerializer
from django.shortcuts import render

class ChatHistoryAPIView(APIView):
    def get(self, request):
        message = Message.objects.all().order_by('-timestamp')
        serializer = MessageSerializer(message, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

#테스트용 뷰
def index(request):
    return render(request, "chat/index.html")