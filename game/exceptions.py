class GameException(Exception):
    """Main Game Exception"""


class PlayerMoveException(GameException):
    """Main Player Move Exception"""


class PlayerHitCards(PlayerMoveException):
    """The player hit cards, It has revealed those same cards."""


class PlayerMissed(PlayerMoveException):
    """The player chose two different cards"""


class CommandException(GameException):
    """Command Game Exception"""


class InvalidArgsException(CommandException):
    """Throw if user passed invalid arguments for specific command"""


class InvalidCommandException(CommandException):
    """Throw if user passed invalid command - command doesn't exist"""


class CardDoesNotExist(GameException):
    """Throw if card doesn't exist in cards list"""


class GameOver(GameException):
    """Game Over Exception"""
