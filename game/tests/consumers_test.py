from channels.testing import ChannelsLiveServerTestCase
from channels.testing import WebsocketCommunicator
from django.contrib.auth.models import User

from cards.models import Card
from room.models import GameRoom, Game
from .. import config
from ..consumers import GameConsumer
from ..player import AIPlayer


class GameConsumerTest(ChannelsLiveServerTestCase):
    def setUp(self) -> None:
        password = 'Password12#$'
        username = 'johnny'
        self.user = User(username=username, email='johnny@gmail.com')
        self.user.set_password(password)
        self.user.save()

        is_logged_in = self.client.login(username=username, password=password)
        self.assertTrue(is_logged_in)

        game = Game.objects.create(player=self.user)
        self.game_room = GameRoom.objects.create(player=self.user, game=game)
        cards_list = [
            'blue', 'red', 'green', 'pink',
            'orange', 'yellow', 'white', 'black'
        ]
        [Card.objects.create(name=name) for name in cards_list]

    async def test_consumer(self) -> None:
        communicator = WebsocketCommunicator(GameConsumer.as_asgi(), f'ws/game/{self.game_room.id}/')
        communicator.scope.update({
            'user': self.user
        })
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        msg = await communicator.receive_json_from()
        self.assertEqual(msg['message'], config.S_START)
        msg = await communicator.receive_json_from()
        size = config.SIZE_OF_BOARD
        self.assertEqual(msg['message'][config.S_BOARD_SIZE], f'{size}x{size}')

        ai_player = AIPlayer()
        count = 0
        while True:
            count += 1
            message = ai_player.sender()
            # print(message)
            await communicator.send_json_to(message)
            content = await communicator.receive_json_from()
            ai_player.receiver(content['message'])
            # print(content['message'])
            if count % 2 == 0:
                content = await communicator.receive_json_from()
                ai_player.receiver(content['message'])
                # print(content['message'])

            if ai_player.is_game_over():
                content = await communicator.receive_json_from()
                self.assertTrue(type(content['message'][config.S_POINTS]) == int)
                content = await communicator.receive_json_from()
                self.assertEqual(content['message'], config.S_END)
                break

        await communicator.disconnect()
