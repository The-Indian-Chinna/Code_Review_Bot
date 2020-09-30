from abc import ABC, abstractmethod
from typing import Dict
from . import CommandPayload


class Command(ABC):
    """Base class for commands interface

    Example Usage:
    ```python
    # commands/hello.py ---------------------------------------------------------------------------
    from commands import Command, CommandPayload, command_registry.register_command

    class HelloCommand(Command):
        # add docstring defining command functionality here

        async def call(self, payload: CommandPayload) -> None:
            # NO docstring is needed here, define command functionality at the class level 
            # docstring
            await payload.gh.post(payload.issue_url + "/comments", data={"body": "Hello human!"})

    command_registry.register_command('hello', HelloCommand())

    # commands/__init__.py ------------------------------------------------------------------------
    from . import hello
    ```
    """

    @abstractmethod
    async def call(self, payload: CommandPayload) -> bool:
        """Executes this specific command. 
        
        Functionality should be defined by the derived class (ex: HelloCommand).

        Args:
            payload (CommandPayload): All data available to this command. See ``CommandPayload``
                for more information 

        Returns:
            bool: True if the command succeeded, False if it did not.
        """
        return False
