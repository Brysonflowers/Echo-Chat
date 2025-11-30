from django.urls import path
from echochatapp.consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat/<str:room_name>/', ChatConsumer.as_asgi()),
    path('ws/private_chat/<str:private_chat_id>/', ChatConsumer.as_asgi()),
]
