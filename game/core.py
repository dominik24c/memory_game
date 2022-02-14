import random
from itertools import product

from .cards import Card, Position, CardMixin
from .command_reader import CommandReaderMixin
from .config import C_SHOW, NUM_OF_CARDS, SIZE_OF_BOARD, \
    NUM_OF_THE_SAME_CARDS, POINTS
from .exceptions import GameOver, InvalidCommandException, \
    GameException

CARDS = ['cat', 'dog', 'deer', 'mouse', 'hamster', 'shark', 'horse', 'cow']


class BoardGeneratorMixin:
    def randomize_cards(self, available_cards: list) -> list:
        n_cards = NUM_OF_CARDS // 2
        if len(available_cards) < n_cards:
            raise Exception("We need 5 different cards at least!")
        random.shuffle(available_cards)
        return available_cards[:n_cards]

    def generate_positions(self) -> list:
        positions = list(product(list(range(SIZE_OF_BOARD)), repeat=NUM_OF_THE_SAME_CARDS))
        random.shuffle(positions)
        return positions

    def generate_boards(self, cards: list, positions: list) -> list[Card]:
        cards_list = []
        for p, c in zip(positions, cards):
            cards.append(Card(c, Position(*p)))
        return cards_list

    def create_boards(self) -> list[Card]:
        cards = self.randomize_cards(CARDS)
        positions = self.generate_positions()
        return self.generate_boards(cards, positions)


class BaseGame(CommandReaderMixin, CardMixin, BoardGeneratorMixin):
    pass


class Game(BaseGame):
    def __init__(self):
        self.__hidden_cards: list[Card] = self.create_boards()
        self.__unhidden_cards: list[Card] = []
        self.points = 0
        self.errors = 0

    @property
    def hidden_cards(self) -> list[Card]:
        return self.__hidden_cards

    @property
    def unhidden_cards(self) -> list[Card]:
        return self.__unhidden_cards

    def clear_unhidden_cards(self) -> None:
        self.__unhidden_cards = []

    def check_the_game_is_over(self) -> None:
        if len(self.hidden_cards) == 0:
            raise GameOver()

    def receive_message_handler(self, msg: str) -> None:
        if msg.startswith(C_SHOW):
            x, y = self.show_command_handler(msg)

            if len(self.unhidden_cards) == 0:
                card = self.get_card_by_position(self.hidden_cards, (x, y))
                self.unhidden_cards.append(card)
            elif len(self.unhidden_cards) == 1:
                card1 = self.get_card_by_position(self.hidden_cards, (x, y))
                card2 = self.unhidden_cards[0]
                if card1 == card2:
                    self.remove_card(self.hidden_cards, card1)
                    self.remove_card(self.hidden_cards, card2)
                    self.points += POINTS
                self.clear_unhidden_cards()
                self.check_the_game_is_over()

            raise Exception("ERROR")
        else:
            raise InvalidCommandException

    def receive_message(self, message: str) -> None:
        try:
            self.receive_message_handler(message.strip())
        except InvalidCommandException:
            self.errors += 1
        except GameException:
            pass
