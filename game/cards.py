from dataclasses import dataclass

from .exceptions import CardDoesNotExist, GameException


@dataclass
class Position:
    __slots__ = ['x', 'y']

    x: int
    y: int


@dataclass
class Card:
    __slots__ = ['name', 'position']

    name: str
    position: Position

    def __str__(self) -> str:
        return f'{self.name} [{self.position.x}:{self.position.y}]'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.name!r},{Position.__class__.__name__}({self.position.x!r},{self.position.y!r}),{self.hidden!r})'

    def __eq__(self, other) -> bool:
        if isinstance(other, Card):
            return self.name == other.name and self.position.x == other.position.x \
                   and self.position.y == other.position.y
        if type(other) == tuple[int, int]:
            return self.position.x == other[0] and self.position.y == other[1]
        raise GameException(f'Incorrect object was passed! It must be instance of {self.__class__.__name__}')


class CardMixin:
    def get_card_by_position(self, cards: list[Card], position: tuple[int, int]):
        cards_tmp = list(filter(lambda c: c == position, cards))
        if len(cards_tmp) != 1:
            raise CardDoesNotExist

        return cards_tmp[0]

    def remove_card(self, cards: list[Card], card: Card) -> None:
        try:
            cards.remove(card)
        except ValueError:
            raise CardDoesNotExist("Cannot remove card!")
