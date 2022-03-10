from unittest import TestCase

from ..cards import Card, Position, CardMixin
from ..exceptions import CardDoesNotExist


class CardTests(TestCase):
    def test_comparing_cards(self) -> None:
        card1 = Card('banana', Position(0, 0))
        card2 = Card('banana', Position(2, 3))
        card3 = Card('orange', Position(1, 2))
        card_tuple = (0, 0)

        self.assertEqual(card1, card2)
        self.assertNotEqual(card1, card3)
        self.assertEqual(card1, card_tuple)

    def test_str_func_of_card(self) -> None:
        card1 = Card('banana', Position(0, 0))
        self.assertEqual(str(card1), f'banana 0:0')


class CardMixinTests(TestCase):
    def test_get_card_by_position(self) -> None:
        card_mixin = CardMixin()
        data = [
            Card('banana', Position(0, 0)),
            Card('apple', Position(2, 4)),
            Card('banana', Position(1, 1))
        ]
        searched_card = (2, 4)
        card = card_mixin.get_card_by_position(data, searched_card)
        self.assertEqual(card.name, 'apple')

        with self.assertRaises(CardDoesNotExist):
            card_mixin.get_card_by_position(data, (3, 3))
