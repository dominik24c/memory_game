from collections import defaultdict

from . import config


class AIPlayer:
    def __init__(self):
        self.__board = defaultdict(list)
        self.__pos_x = 0
        self.__pos_y = 0
        self.__moves = 0
        self.__cards = []
        self.hits = config.NUM_OF_THE_SAME_CARDS * config.SIZE_OF_BOARD
        self.__chosen_cards_to_reveal = []
        self.flag = False

    def clear_unhidden_cards(self) -> None:
        self.__cards = []

    def is_game_over(self) -> bool:
        return self.hits == 0

    def removes_cards_from_board(self) -> None:
        card_name = self.__cards[0][0]
        del self.__board[card_name]

    def find_cards(self) -> None:
        try:
            key = list(self.__board.keys())[0]
            for pos in self.__board[key]:
                self.__chosen_cards_to_reveal.append(pos)
        except IndexError:
            '''board is empty'''
            pass

    def receiver(self, message: str) -> None:
        if isinstance(message, dict):
            msg = message.get(config.S_CARD)
            if msg is not None:
                name = msg.split()[0]
                self.__cards.append((name, self.__pos_x, self.__pos_y))
                if self.__moves <= 16 and not self.flag:
                    self.__board[name].append((self.__pos_x, self.__pos_y))
                    self.go_through_the_entire_board()
                    if self.__moves == 16:
                        self.flag = True
                        self.find_cards()
        elif message.startswith(config.S_HIT):
            self.hits -= 1
            self.removes_cards_from_board()
            self.clear_unhidden_cards()
            if self.__moves > 16:
                self.find_cards()
        elif message.startswith(config.S_MISSED):
            self.clear_unhidden_cards()

    def go_through_the_entire_board(self) -> None:
        if self.__pos_x < config.SIZE_OF_BOARD - 1:
            self.__pos_x += 1
        else:
            self.__pos_x = 0
            if self.__pos_y < config.SIZE_OF_BOARD - 1:
                self.__pos_y += 1

    def sender(self) -> dict:
        self.__moves += 1
        if self.__moves > 16:
            card = self.__chosen_cards_to_reveal[0]
            self.__pos_x, self.__pos_y = card[0], card[1]
            self.__chosen_cards_to_reveal.pop(0)

        message = f'{config.C_SHOW} {self.__pos_x} {self.__pos_y}'
        # print(self.__board)
        return {'message': message}
