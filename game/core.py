import random
from itertools import product

from cards.models import Card as CardModel
from .cards import Card, Position, CardMixin
from .command_reader import CommandReaderMixin
from .config import C_SHOW, NUM_OF_CARDS, SIZE_OF_BOARD, \
    NUM_OF_THE_SAME_CARDS, S_OK, S_ERROR, S_CARDS, \
    S_HIT, S_MISSED, S_POINTS, S_END, POINTS, PENALTY_POINTS
from .exceptions import GameOver, InvalidCommandException, \
    GameException, PlayerMoveException, PlayerMissed, PlayerHitCards


class BoardGeneratorMixin:
    def randomize_cards(self, available_cards: list[str]) -> list:
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
            cards_list.append(Card(c, Position(*p)))
        # print(cards_list)
        return cards_list

    def create_boards(self, cards_list: list[CardModel]) -> list[Card]:
        cards_str = list(map(lambda card: card.name, cards_list))
        cards = self.randomize_cards(cards_str)
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

    def init_hidden_cards(self, cards: list[CardModel]):
        self.hidden_cards = self.create_boards(cards)

    @property
    def hidden_cards(self) -> list[Card]:
        return self.__hidden_cards

    @hidden_cards.setter
    def hidden_cards(self, value: list) -> None:
        self.__hidden_cards = value

    @property
    def unhidden_cards(self) -> list[Card]:
        return self.__unhidden_cards

    def clear_unhidden_cards(self) -> None:
        self.__unhidden_cards = []

    def check_the_game_is_over(self) -> None:
        if len(self.hidden_cards) == 0:
            raise GameOver()

    def get_cards_message(self) -> dict:
        cards_msg = {S_CARDS: []}
        print(self.hidden_cards)
        for card in self.hidden_cards:
            print(card)
            cards_msg[S_CARDS].append({
                'name': card.name,
                'position': {
                    'x': card.position.x,
                    'y': card.position.y
                }
            })
        return cards_msg

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
                    self.clear_unhidden_cards()
                    self.check_the_game_is_over()
                    raise PlayerHitCards
                else:
                    self.total_points -= PENALTY_POINTS
                    self.clear_unhidden_cards()
                    raise PlayerMissed
            else:
                raise Exception("ERROR")
        else:
            raise InvalidCommandException

    def receive_message(self, message: str) -> str | tuple[str, str] | tuple[str, str, dict, str]:
        try:
            self.receive_message_handler(message.strip())
        except GameOver:
            return S_OK, S_HIT, {S_POINTS: self.total_points}, S_END
        except PlayerMoveException as e:
            if isinstance(e, PlayerHitCards):
                return S_OK, S_HIT
            elif isinstance(e, PlayerMissed):
                return S_OK, S_MISSED
        except GameException as e:
            self.errors += 1
            print(e)
            return S_ERROR
        except Exception as e:
            print(e)
            return S_ERROR
        else:
            return S_OK
