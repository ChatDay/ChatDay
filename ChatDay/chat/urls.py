from django.urls import path
from . import views


urlpatterns = [
    path('history/',views.ChatHistoryAPIView.as_view(), name="chat_history"),
    path('index/', views.index, name='index') #테스트용
]