import pytest
from typing import List
from cam2_code_review_bot.commands import (
    is_registered_command,
    register_command,
    Command,
    CommandPayload,
)


class ExampleCommand(Command):
    async def call(self, payload: CommandPayload) -> bool:
        print("this is an example command")
        return True


register_command("example", ExampleCommand)


def test_register_command():
    """Checks that the example command was registered properly by the system
    """
    assert is_registered_command("example")


def test_all_commands_are_registered():
    """Checks that all commands defined by optimus are successfully registered 
    """

    defined_commands: List[str] = [
        "hello",
        "assign",
        "init",
        "lint",
        "report",
        "show",
        "parent",
        "open",
        "roles",
    ]

    for command in defined_commands:
        assert is_registered_command(command)
