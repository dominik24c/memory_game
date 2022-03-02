from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth.models import User

from cards.models import Card
from game.config import S_START
from game.core import Game
from room.models import GameRoom


@database_sync_to_async
def get_cards() -> list[Card]:
    return list(Card.objects.all())


@database_sync_to_async
def get_user_by_username(username: str) -> User:
    return User.objects.get(username=username)


@database_sync_to_async
def delete_room_game_by_user(user: User) -> None:
    GameRoom.objects.filter(player=user).first().delete()


class GameConsumer(AsyncJsonWebsocketConsumer):
    game = Game()
    user: User

    async def send_msg(self, content: str | dict) -> None:
        await self.send_json({"message": content})

    async def connect(self):
        await self.accept()
        self.user = await get_user_by_username(self.scope['user'])
        cards = await get_cards()
        self.game.init_hidden_cards(cards)
        await self.send_msg(S_START)
        await self.send_msg(self.game.get_cards_message())

    async def disconnect(self, code):
        # """Remove game room"""
        await delete_room_game_by_user(self.user)

    async def receive_json(self, content, **kwargs):
        print(content)
        message = content['message']
        answer = self.game.receive_message(message)
        await self.send_msg(answer)
