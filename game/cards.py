from dataclasses import dataclass
from weakref import WeakKeyDictionary

from .exceptions import CardDoesNotExist, GameException


@dataclass(frozen=True)
class Position:
    __slots__ = ['x', 'y']

    x: int
    y: int


@dataclass(frozen=True)
class Card:
    __slots__ = ['name', 'position']

    name: str
    position: Position

    def __str__(self) -> str:
        return f'{self.name} {self.position.x}:{self.position.y}'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.name!r},{Position.__class__.__name__}({self.position.x!r},' \
               f'{self.position.y!r}))'

    def __eq__(self, other) -> bool:
        if isinstance(other, Card):
            return self.name == other.name and \
                   not (self.position.x == other.position.x and self.position.y == other.position.y)
        if isinstance(other, tuple) and list(map(type, other)) == [int, int]:
            return self.position.x == other[0] and self.position.y == other[1]
        raise GameException(f'Incorrect object was passed! It must be instance of {self.__class__.__name__}')


class CardMixin:
    def get_card_by_position(self, cards: list[Card], position: tuple[int, int]):
        cards_tmp = list(filter(lambda c: c == position, cards))
        if len(cards_tmp) != 1:
            raise CardDoesNotExist

        return cards_tmp[0]
