import json
import subprocess
from typing import List, Dict, Any
from abc import ABC, abstractmethod
from . import StaticError, StaticAnalyzer, StaticTool


class ProspectorTool(StaticTool):
    """Implementation of Prospector static analysis tool

    Prospector is a static analysis tool that analyzes Python code and output information about errors, potential problems, convention violations and complexity.
    """

    def __init__(self):
        super(ProspectorTool, self).__init__("prospector")

    def load_config(self, config: Dict[str, Any]) -> None:
        """Loads the specified ``configs`` for Prospector

        Configs:
            file_path (str): The relative path to the file to run prospector on. This must be a 
            ".py" file

        Args:
            config (Dict[str, Any]): Configs for prospector, (see above)

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
        """Runs Prospector with the given configs set by `load_config`

        Returns:
            List[StaticError]: a list of all dead code errors reported by Prospector

        """
        
        # runs prospector on the configured file and returns the output as a json string
        process = subprocess.Popen(
            "prospector -o json --strictness veryhigh --no-autodetect " + self.file_path, shell=True, stdout=subprocess.PIPE
        )
        stdout, _ = process.communicate()

        # converts the json string to a readable json object
        data: Dict[str, Any] = json.loads(stdout)

        error_list = []

        for error_data in data['messages']:
            static_error: StaticError = StaticError(
                file_path=error_data['location']['path'],
                line_no=error_data['location']['line'],
                error_name=error_data['code'],
                error_description=error_data['message'],
                tool_name=error_data['source']
            )

            error_list.append(static_error)

        return error_list
