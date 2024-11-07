from django.urls import path
from . import views


urlpatterns = [
    path('history/',views.ChatHistoryAPIView.as_view(), name="chat_history"),
    path('current-topic/', views.CurrentTopicView.as_view(), name='current-topic'),
]