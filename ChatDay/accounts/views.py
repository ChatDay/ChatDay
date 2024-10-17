from django.shortcuts import render
from django.contrib.auth import get_user_model
from .serializers import SignupSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

class SignupView(CreateAPIView):
    model = get_user_model()
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]
