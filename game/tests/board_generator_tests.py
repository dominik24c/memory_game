from unittest import TestCase

from ..cards import Card
from ..config import NUM_OF_CARDS
from ..core import BoardGeneratorMixin
from ..exceptions import InvalidLengthOfCardsAndPositions
from cards.models import Card as CardModel


class BoardGeneratorMixinTest(TestCase):
    def test_generate_positions(self) -> None:
        board_generator = BoardGeneratorMixin()
        positions = board_generator.generate_positions()
        self.assertEqual(len(positions), NUM_OF_CARDS)

    def test_generate_boards(self) -> None:
        positions = [(0, 0), (1, 0), (0, 1), (1, 1)]
        cards = ['banana', 'apple', 'apple', 'banana']
        board_generator = BoardGeneratorMixin()
        cards_list = board_generator.generate_boards(cards, positions)

        self.assertEqual(len(cards_list), len(positions))
        for card in cards_list:
            self.assertIsInstance(card, Card)

        cards.pop(0)
        with self.assertRaises(InvalidLengthOfCardsAndPositions):
            board_generator.generate_boards(cards, positions)

    def test_create_boards(self) -> None:
        name_of_card = 'banana'
        names_of_cards = [name_of_card]*(NUM_OF_CARDS//2)
        cards = [CardModel(name=name) for name in names_of_cards]
        board_generator = BoardGeneratorMixin()
        cards_list = board_generator.create_boards(cards)

        self.assertEqual(len(cards_list), len(cards) * 2)
        for card in cards_list:
            self.assertEqual(card.name, name_of_card)
