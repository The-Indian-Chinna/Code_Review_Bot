import json
import subprocess
from typing import List, Dict, Any
from . import StaticError, StaticAnalyzer, StaticTool


class MyPyTool(StaticTool):
    """MyPy static analysis tool

    MyPy is a static analysis tool designed to typecheck python code

    """

    def __init__(self):
        super(MyPyTool, self).__init__("mypy")

    def load_config(self, config: Dict[str, Any]) -> None:
        """Loads the specified ``configs`` for mypy

        Configs:
            file_path (str): The relative path to the file to run mypy on. This must be a ".py" file

        Args:
            config (Dict[str, Any]): Configs for mypy, (see above)

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
        """Runs mypy with the given configs set by `load_config`

        Returns:
            [StaticError]: a list of all dead code errors reported by mypy

        """

        process = subprocess.Popen(
            "mypy " + self.file_path, shell=True, stdout=subprocess.PIPE
        )
        stdout, _ = process.communicate()

        # list of static errors reported by vulture
        error_list = []
        
        for output_encoded in stdout.splitlines():

            # decode the string output
            output:str = output_encoded.decode()
            
            if output.startswith('Found'):
                continue

            partition: str = output.partition(':')
            file_path: str = partition[0]

            # remove the output that was parsed
            output = partition[2]
            partition = output.partition(':')
            
            line_number: int = int(partition[0])

            output = partition[2]
            partition = output.partition('error: ')

            error_description: str = partition[2]

            static_error: StaticError = StaticError(
                file_path=file_path,
                line_no=line_number,
                error_name='MyPy Error',
                error_description=error_description,
            )

            error_list.append(static_error)

        return error_list
