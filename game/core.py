import random
from itertools import product

from cards.models import Card as CardModel
from .cards import Card, Position, CardMixin
from .command_reader import CommandReaderMixin
from .config import C_SHOW, SIZE_OF_BOARD, \
    NUM_OF_THE_SAME_CARDS, S_ERROR, S_CARD, \
    S_HIT, S_MISSED, S_POINTS, S_END, POINTS, PENALTY_POINTS
from .exceptions import InvalidCommandException, \
    GameException, PlayerMoveException, PlayerMissed, \
    PlayerHitCards, RevealFirstCard, InvalidLengthOfCardsAndPositions


class BoardGeneratorMixin:
    def generate_positions(self) -> list:
        positions = list(product(list(range(SIZE_OF_BOARD)), repeat=NUM_OF_THE_SAME_CARDS))
        random.shuffle(positions)
        return positions

    def generate_boards(self, cards: list[str], positions: list) -> list[Card]:
        cards_list = []
        if len(positions) != len(cards):
            raise InvalidLengthOfCardsAndPositions("Length of cards and positions are difference!")
        for p, c in zip(positions, cards):
            cards_list.append(Card(c, Position(*p)))
        return cards_list

    def create_boards(self, cards_list: list[CardModel]) -> list[Card]:
        cards = list(map(lambda card: card.name, cards_list))
        positions = self.generate_positions()
        return self.generate_boards(cards + cards, positions)


class BaseGame(CommandReaderMixin, CardMixin, BoardGeneratorMixin):
    pass


class Game(BaseGame):
    def __init__(self):
        self.__hidden_cards: list[Card] = []
        self.__unhidden_cards: list[Card] = []
        self.total_points = POINTS
        self.errors = 0

    def init_hidden_cards(self, cards: list[CardModel]) -> None:
        self.hidden_cards = self.create_boards(cards)

    @property
    def hidden_cards(self) -> list[Card]:
        return self.__hidden_cards

    @hidden_cards.setter
    def hidden_cards(self, value: list[Card]) -> None:
        self.__hidden_cards = value

    @property
    def unhidden_cards(self) -> list[Card]:
        return self.__unhidden_cards

    @unhidden_cards.setter
    def unhidden_cards(self, value: list[Card]) -> None:
        self.__unhidden_cards = value

    def clear_unhidden_cards(self) -> None:
        self.unhidden_cards = []

    def remove_cards(self) -> None:
        for card in self.unhidden_cards:
            self.hidden_cards.remove(card)

    def check_the_game_is_over(self) -> bool:
        return True if len(self.hidden_cards) == 0 else False

    def get_first_chosen_card_message(self) -> dict:
        return {S_CARD: f'{self.unhidden_cards[0]}'}

    def get_second_chosen_card_message(self) -> dict:
        return {S_CARD: f'{self.unhidden_cards[1]}'}

    def receive_message_handler(self, msg: str) -> None:
        if msg.startswith(C_SHOW):
            x, y = self.show_command_handler(msg)
            if len(self.unhidden_cards) == 0:
                card = self.get_card_by_position(self.hidden_cards, (x, y))
                self.unhidden_cards.append(card)
                raise RevealFirstCard
            elif len(self.unhidden_cards) == 1:
                card1 = self.get_card_by_position(self.hidden_cards, (x, y))
                self.unhidden_cards.append(card1)
                card2 = self.unhidden_cards[0]
                if card1 == card2:
                    raise PlayerHitCards
                else:
                    self.total_points -= PENALTY_POINTS
                    raise PlayerMissed
            else:
                raise Exception("Error")
        else:
            raise InvalidCommandException

    def receive_message(self, message: str) -> str | dict | tuple[dict, str] | tuple[dict, str, dict, str]:
        try:
            self.receive_message_handler(message.strip())
        except PlayerMoveException as e:

            if isinstance(e, PlayerHitCards):
                card_msg = self.get_second_chosen_card_message()
                self.remove_cards()
                self.clear_unhidden_cards()
                if self.check_the_game_is_over():
                    return card_msg, S_HIT, {S_POINTS: self.total_points}, S_END
                return card_msg, S_HIT

            elif isinstance(e, PlayerMissed):
                card_msg = self.get_second_chosen_card_message()
                self.clear_unhidden_cards()
                return card_msg, S_MISSED

            elif isinstance(e, RevealFirstCard):
                return self.get_first_chosen_card_message()

        except GameException as e:
            self.errors += 1
            # print(e)
            return S_ERROR

        except Exception as e:
            # print(e)
            return S_ERROR
