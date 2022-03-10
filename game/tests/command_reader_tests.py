from unittest import TestCase

from ..command_reader import int_try_parse, CommandReaderMixin
from ..config import C_SHOW
from ..exceptions import InvalidArgsException


class ParsingTest(TestCase):
    def test_int_try_parse(self) -> None:
        test_value = '3'
        value, status = int_try_parse(test_value)

        self.assertTrue(status)
        self.assertIsInstance(value, int)
        self.assertEqual(value, int(test_value))

        test_value = '3oed'
        value, status = int_try_parse(test_value)

        self.assertFalse(status)
        self.assertIsInstance(value, str)


class CommandReaderMixinTest(TestCase):
    def test_show_command_handler(self) -> None:
        command_reader = CommandReaderMixin()
        command = f'{C_SHOW} 2 3'
        x, y = command_reader.show_command_handler(command)
        self.assertEqual(x, 2)
        self.assertEqual(y, 3)

        command = f'{C_SHOW} sd ok'
        with self.assertRaises(InvalidArgsException):
            command_reader.show_command_handler(command)

        command = f'{C_SHOW} 2'
        with self.assertRaises(InvalidArgsException):
            command_reader.show_command_handler(command)

        command = f'{C_SHOW} 2 x4e'
        with self.assertRaises(InvalidArgsException):
            command_reader.show_command_handler(command)


