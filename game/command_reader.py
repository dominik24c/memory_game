from config import C_SHOW
from .exceptions import InvalidArgsException


def int_try_parse(value: str) -> tuple[int | str, bool]:
    try:
        return int(value), True
    except ValueError:
        return value, False


class CommandReaderMixin:
    def show_command_handler(self, command: str) -> tuple[int, int]:
        result = command.split(' ')
        result.remove(C_SHOW)
        if len(result) != 2:
            raise InvalidArgsException(f"Invalid arguments for {C_SHOW} command")

        x = result[0].strip()
        y = result[1].strip()

        x, parsing_is_success_x = int_try_parse(x)
        y, parsing_is_success_y = int_try_parse(y)

        if parsing_is_success_x and parsing_is_success_y:
            return x, y
        raise InvalidArgsException("Arguments must be integer!")
