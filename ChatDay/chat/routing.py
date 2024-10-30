from django.urls import path
from . import consumers
from django.urls import re_path

websocket_urlpatterns = [
        re_path(r'ws/chat/$', consumers.ChatConsumer.as_asgi()),
]

# # routing.py (WebSocket 경로 설정)
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.urls import re_path
# from channels.auth import AuthMiddlewareStack
# from .consumers import ChatConsumer

# application = ProtocolTypeRouter({
#     'websocket': AuthMiddlewareStack(
#         URLRouter([
#             re_path(r'ws/chat/$', ChatConsumer.as_asgi()),
#         ])
#     ),
# })
