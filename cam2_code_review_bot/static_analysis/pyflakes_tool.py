import json
import subprocess
from typing import List, Dict, Any
from abc import ABC, abstractmethod
from . import StaticError, StaticAnalyzer, StaticTool


class PyflakesTool(StaticTool):
    """Pyflakes static analysis tool

    Pyflakes is a static analysis tool designed to detect compile time code errors in python

    """

    def __init__(self):
        super(PyflakesTool, self).__init__("pyflakes")

    def load_config(self, config: Dict[str, Any]) -> None:
        """Loads the specified ``configs`` for Pyflakes

        Configs:
            file_path (str): The relative path to the file to run Pyflakes on. This must be a ".py" file

        Args:
            config (Dict[str, Any]): Configs for Pyflakes, (see above)

        Raises:
            ValueError: If "file_path" config is not included in the config file
            ValueError: If "file_path" config is not a python file (".py" extension)

        """
        if not "file_path" in config:
            raise ValueError('Invalid config file. [file_type] not defined.')

        self.file_path = config["file_path"]

        if not '.py' in self.file_path:
            raise ValueError('Invalid file type provided. File must have the extension ".py"')

    def run(self) -> List[StaticError]:
        """Runs Pyflakes with the given configs set by `load_config`

        Returns:
            [StaticError]: a list of all dead code errors reported by Pyflakes

        """

        process = subprocess.Popen(
            "pyflakes " + self.file_path, shell=True, stdout=subprocess.PIPE
        )
        stdout, _ = process.communicate()

        # list of static errors reported by vulture
        error_list = []
        
        for output_encoded in stdout.splitlines():

            # decode the string output
            output:str = output_encoded.decode()
            partition: str = output.partition(':')

            file_path: str = partition[0]
            output = partition[2]
            partition = output.partition(':')

            line_number: int = int(partition[0])
            output = partition[2]
            partition = output.partition(' ')

            error_description: str = partition[2]
            

            static_error: StaticError = StaticError(
                file_path=file_path,
                line_no=line_number,
                error_name='Pyflakes Error',
                error_description=error_description,
            )
            error_list.append(static_error)

        return error_list
