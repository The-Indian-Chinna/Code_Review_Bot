from . import Command
from typing import Dict

__COMMAND_REGISTRY: Dict[str, Command] = dict()


def register_command(name: str, command: Command) -> None:
    """Defines a new command in the registry

    Args:
        name (str): The name of the command. Also the name used to 
            call the command

        command (Command): The command itself. This is where the functionality
            for the command is defined (see command.py)
    
    Raises:
        ValueError: If a command with `name` is already registered
    """
    if name in __COMMAND_REGISTRY.keys():
        raise ValueError("Command with name [" + name + "] already exists")
    __COMMAND_REGISTRY[name] = command


def is_registered_command(name: str) -> bool:
    """Checks if a command is registered

    Returns:
        bool: True if the command with `name` is registered
    """
    return name in __COMMAND_REGISTRY.keys()


def get_command(name: str) -> Command:
    """Returns the instantiated Command object registered with `name`

    Args:
        name (str): The name of the command. 

    Returns:
        Command: The command object registered under `name`
    """
    if not is_registered_command(name):
        raise ValueError("Command with name [" + name + "] already exists")
    return __COMMAND_REGISTRY[name]
