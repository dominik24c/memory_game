from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Game, GameRoom


class BaseGameView(TestCase):
    def setUp(self) -> None:
        self.password = 'Password123!'
        self.user = User.objects.create(
            username='test_user', email='test@test.com')
        self.user.set_password(self.password)
        self.user.save()
        is_logged_in = self.client.login(username=self.user.username, password=self.password)
        self.assertTrue(is_logged_in)


class GameViewTests(BaseGameView):
    def test_game_view(self) -> None:
        game_room = GameRoom.objects.create(player=self.user)

        response = self.client.get(reverse('game:game', kwargs={'game_room': game_room.id}))
        body = response.content.decode('utf-8')
        self.assertEqual(response.status_code, 200)
        self.assertIn('<h4 class="mt-2">Game</h4>', body)


class GameDashboardView(BaseGameView):
    def setUp(self) -> None:
        super().setUp()
        user1 = User.objects.create(username='test_user1', email='test1@test.com')
        game1 = Game(player=user1)
        game2 = Game(player=self.user)
        Game.objects.bulk_create((game1, game2), 2)
        game1.points = 50
        game2.points = 75
        game1.save()
        game2.save()
        self.all_games = Game.objects.all()
        self.games = Game.objects.filter(player=self.user)

    def test_dashboard_standings_view(self) -> None:
        response = self.client.get(reverse('game:dashboard'))
        body = response.content.decode('utf-8')
        self.assertIn('<div id="standings">', body)
        self.assertIn('<h3>Standings</h3>', body)
        sum_of_points = sum(map(lambda g: g.points, self.games))
        self.assertIn(f'<th scope="row">{self.user.username}</th>', body)
        self.assertIn(f'<td>{sum_of_points}</td>', body)
        self.assertIn(f'<td>{sum_of_points / len(self.games):.2f}</td>', body)

    def _test_case_of_game_info(self, game: Game, body: str, first_row: str = 'td'):
        scope_row = ''
        if first_row == 'th':
            scope_row = f' scope="row"'
        self.assertIn(f'<{first_row}{scope_row}>{game.points}</{first_row}>', body)
        self.assertIn(f'<td>{game.started_at:%H:%M:%S %d.%m.%Y}</td>', body)
        self.assertIn(f'<td>{game.ended_at:%H:%M:%S %d.%m.%Y}</td>', body)

    def test_dashboard_games_view(self) -> None:
        response = self.client.get(reverse('game:dashboard') + "?search=games")
        body = response.content.decode('utf-8')
        self.assertIn('<h3>Games</h3>', body)
        for game in self.all_games:
            self.assertIn(f'<th scope="row">{game.player.username}</th>', body)
            self._test_case_of_game_info(game, body)

    def test_dashboard_user_games_view(self) -> None:
        response = self.client.get(reverse('game:dashboard') + "?search=player-games")
        body = response.content.decode('utf-8')
        self.assertIn(f'<h3>Your games - {self.user}</h3>', body)
        for game in self.games:
            self._test_case_of_game_info(game, body, first_row='th')
