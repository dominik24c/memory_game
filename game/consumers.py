from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth.models import User

from cards.models import Card
from game.config import S_START, S_END, SIZE_OF_BOARD, \
    NUM_OF_THE_SAME_CARDS, S_BOARD_SIZE, S_POINTS, \
    PENALTY_POINTS_FOR_EXIT
from game.core import Game
from room.models import Game as GameModel
from room.models import GameRoom


@database_sync_to_async
def get_cards() -> list[Card]:
    amount = SIZE_OF_BOARD * NUM_OF_THE_SAME_CARDS
    return list(Card.objects.all().order_by("?")[:amount])


@database_sync_to_async
def get_user_by_username(username: str) -> User:
    return User.objects.filter(username=username) \
        .select_related('game_room').first()


@database_sync_to_async
def delete_room_game_by_user(user: User) -> None:
    game_room = GameRoom.objects.select_related('game').filter(player=user).first()
    if game_room is not None:
        game = game_room.game
        if game.points == -1:
            game.points = PENALTY_POINTS_FOR_EXIT
            game.save()
        game_room.delete()


@database_sync_to_async
def save_game_points(user: User, points: int) -> None:
    game = GameModel.objects.filter(game_room=user.game_room).first()
    game.points = points
    game.save()


class GameConsumer(AsyncJsonWebsocketConsumer):
    game: Game = None
    user: User

    async def send_msg(self, content: str | dict) -> None:
        await self.send_json({"message": content})

    async def connect(self):
        await self.accept()
        # initialize and start game
        self.game = Game()
        self.user = await get_user_by_username(self.scope['user'])
        cards = await get_cards()
        self.game.init_hidden_cards(cards)
        await self.send_msg(S_START)
        await self.send_msg({S_BOARD_SIZE: f'{SIZE_OF_BOARD}x{SIZE_OF_BOARD}'})

    async def disconnect(self, code):
        # """Remove game room"""
        # print('Disconnect')
        await delete_room_game_by_user(self.user)

    async def receive_json(self, content, **kwargs):
        # print(f'Content {content}')
        message = content['message']
        answer = self.game.receive_message(message)
        # print(f'Answer {answer}')
        if isinstance(answer, tuple):
            for a in answer:
                await self.send_msg(a)
                if isinstance(a, dict):
                    points = a.get(S_POINTS)
                    if points is not None:
                        await save_game_points(self.user, points)
                elif a == S_END:
                    await self.close()
        else:
            await self.send_msg(answer)
