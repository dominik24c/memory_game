from unittest import TestCase

from cards.models import Card as CardModel
from .. import exceptions
from ..cards import Card, Position
from ..config import S_CARD, C_SHOW, PENALTY_POINTS, \
    POINTS, S_ERROR, S_HIT, S_MISSED, S_END, S_POINTS
from ..core import Game


class GameTest(TestCase):
    def setUp(self) -> None:
        self.game = Game()
        names_of_cards = [
            'banana', 'orange', 'apple', 'carrot',
            'melon', 'fish', 'lamb', 'chicken'
        ]
        self.cards = [CardModel(name=name) for name in names_of_cards]
        self.game.init_hidden_cards(self.cards)

    def test_init_hidden_cards(self) -> None:
        self.assertEqual(len(self.game.hidden_cards), len(self.cards) * 2)

    def test_clear_unhidden_cards(self):
        self.game.unhidden_cards = [
            self.game.hidden_cards[0],
            self.game.hidden_cards[1]
        ]

        self.game.clear_unhidden_cards()

        self.assertEqual(len(self.game.unhidden_cards), 0)

    def test_remove_cards(self) -> None:
        length_before_removing_cards = len(self.game.hidden_cards)
        self.game.unhidden_cards = [
            Card('banana', Position(0, 1)),
            Card('banana', Position(0, 0))
        ]
        self.game.remove_cards()

        self.assertEqual(len(self.game.hidden_cards), length_before_removing_cards - 2)

    def test_check_the_game_is_over(self) -> None:
        self.assertFalse(self.game.check_the_game_is_over())
        self.game.hidden_cards = []
        self.assertTrue(self.game.check_the_game_is_over())

    def test_get_first_chosen_card_message_and_get_second_chosen_card_message(self) -> None:
        card1 = Card('banana', Position(0, 1))
        card2 = Card('orange', Position(0, 0))
        self.game.unhidden_cards = [card1, card2]

        message = self.game.get_first_chosen_card_message()
        self.assertEqual(message[S_CARD], str(card1))

        message = self.game.get_second_chosen_card_message()
        self.assertEqual(message[S_CARD], str(card2))

    def test_receive_message_handler_unknown_command(self) -> None:
        with self.assertRaises(exceptions.InvalidCommandException):
            self.game.receive_message_handler("UNKNOWN COMMAND")

    def test_receive_message_handler_show_command_with_invalid_args(self) -> None:
        with self.assertRaises(exceptions.InvalidArgsException):
            self.game.receive_message_handler(f'{C_SHOW} 3')

    def _show_first_card(self) -> Card:
        with self.assertRaises(exceptions.RevealFirstCard):
            self.game.receive_message_handler(f'{C_SHOW} 1 1')
        self.assertEqual(len(self.game.unhidden_cards), 1)
        searched_card = self.game.unhidden_cards[0]
        second_card = [card for card in self.game.hidden_cards if card == searched_card][0]
        return second_card

    def test_receive_message_handler_show_player_hit_cards(self) -> None:
        card = self._show_first_card()
        with self.assertRaises(exceptions.PlayerHitCards):
            self.game.receive_message_handler(f'{C_SHOW} {card.position.x} {card.position.y}')

        self.assertEqual(len(self.game.unhidden_cards), 2)

    def test_receive_message_handler_show_player_missed(self) -> None:
        card1 = self._show_first_card()
        second_card = [card for card in self.game.hidden_cards if card.name != card1.name][0]

        with self.assertRaises(exceptions.PlayerMissed):
            self.game.receive_message_handler(f'{C_SHOW} {second_card.position.x} {second_card.position.y}')

        self.assertEqual(len(self.game.unhidden_cards), 2)
        self.assertEqual(self.game.total_points, POINTS - PENALTY_POINTS)

    def test_receive_message_invalid_command(self) -> None:
        msg = self.game.receive_message(f'{C_SHOW} 1')
        self.assertEqual(msg, S_ERROR)
        msg = self.game.receive_message('UNKNOWN 1')
        self.assertEqual(msg, S_ERROR)

    def _show_first_card_for_testing_receive_message(self, x: int = 0, y: int = 0) -> Card:
        msg = self.game.receive_message(f'{C_SHOW} {x} {y}')
        first_revealed_card = self.game.unhidden_cards[0]
        self.assertEqual(msg[S_CARD], f'{first_revealed_card}')
        second_card = [card for card in self.game.hidden_cards if card == first_revealed_card][0]
        return second_card

    def test_receive_message_valid_command_player_hit_cards(self) -> None:
        length_of_cards = len(self.game.hidden_cards)
        second_card = self._show_first_card_for_testing_receive_message()
        msg = self.game.receive_message(f'{C_SHOW} {second_card.position.x} {second_card.position.y}')
        self.assertIsInstance(msg, tuple)
        self.assertEqual(msg[0][S_CARD], f'{second_card}')
        self.assertEqual(msg[1], f'{S_HIT}')
        self.assertEqual(len(self.game.unhidden_cards), 0)
        self.assertEqual(len(self.game.hidden_cards), length_of_cards - 2)

    def test_receive_message_valid_command_player_missed(self) -> None:
        card1 = self._show_first_card_for_testing_receive_message()
        second_card = [card for card in self.game.hidden_cards if card.name != card1.name][0]

        msg = self.game.receive_message(f'{C_SHOW} {second_card.position.x} {second_card.position.y}')
        self.assertIsInstance(msg, tuple)
        self.assertEqual(msg[0][S_CARD], f'{second_card}')
        self.assertEqual(msg[1], f'{S_MISSED}')
        self.assertEqual(self.game.total_points, POINTS - PENALTY_POINTS)
        self.assertEqual(len(self.game.unhidden_cards), 0)

    def test_receive_message_end_game(self) -> None:
        self.game.hidden_cards = [
            Card('banana', Position(0, 0)),
            Card('banana', Position(0, 1))
        ]
        cards = self.game.hidden_cards
        card_msg_cmd = str(cards[1])

        _ = self._show_first_card_for_testing_receive_message(x=0, y=0)
        msg = self.game.receive_message(f'{C_SHOW} {cards[1].position.x} {cards[1].position.y}')

        self.assertEqual(msg[0][S_CARD], f'{card_msg_cmd}')
        self.assertEqual(msg[1], S_HIT)
        self.assertEqual(msg[2][S_POINTS], POINTS)
        self.assertEqual(msg[3], S_END)
        self.assertEqual(len(self.game.unhidden_cards), 0)
        self.assertEqual(len(self.game.hidden_cards), 0)
