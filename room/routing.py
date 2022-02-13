from django.urls import path

from game.consumers import GameConsumer

websocket_urlpatterns = [
    path(r'ws/game/<str:room_id>/', GameConsumer.as_asgi()),
]
