import json
from typing import Dict, List
from . import StaticError, StaticTool
from tabulate import tabulate

class StaticAnalyzer:
    """Public API object for static analysis

    All supported functionality for static analysis will be defined in this class.

    """
    
    def __init__(self):
        self.__tools: Dict[str, StaticTool] = dict()
        pass

    def add_tool(self, tool: StaticTool, override: bool = False) -> None:
        """Adds a static tool to this analyzer

        Args:
            tool (StaticTool): the tool being added. it will 
                be defined by its `name` property

            override (bool, default=False): if set to true, and a tool with the property `name`
             already exists. the existing tool will be over-written with `tool`. if set to False and
             tool with the property `name` already exists a value error will be thrown (see below).
        
        Raises:
            ValueError: tool exists in analyzer and override is set to False

        """
        if tool.name in self.__tools.keys() and not override:
            raise ValueError('tool already exists but override is set to False')
        self.__tools[tool.name] = tool
    
    def configure_tool_from_file(self, tool_name: str, config_file_path: str) -> None:
        """Configues an existing tool in this analyzer

        Args:
            tool_name (str): the name of the tool being configured
            config_file_path (str): the path to the config file

        Raises:
            ValueError: if the tool is not present in this static analyzer

        """
        tool: StaticTool = self.get_tool(tool_name)
        if tool is None:
            raise ValueError('the tool [' + tool_name + '] does not exist in this static analyzer.')
        tool.load_config_from_file(config_file_path)

    def configure_tool(self, tool_name: str, config: json) -> None:
        """Configures an existing tool in this analyzer

        Args:
            tool_name (str): the name of the tool being configured
            config (json): the configs for this tool
        
        Raises:
            ValueError: if the tool is not present in this static analyzer

        """
        tool: StaticTool = self.get_tool(tool_name)
        if tool is None:
            raise ValueError('the tool [' + tool_name + '] does not exist in this static analyzer.')
        tool.load_config(config)

    def get_tool(self, tool_name: str) -> StaticTool:
        """Gets the tool object named `tool_name`

        Args:
            tool_name (str): the name of the tool being retrieved
            
        Returns:
            StaticTool: on success it returns a StaticTool object with 
                the name `tool_name` and on failure it returns None

        """
        if tool_name in self.__tools.keys():
            return self.__tools.get(tool_name)
        else:
            return None

    def remove_tool(self, tool_name: str) -> bool:
        """Removes the tool with the name `tool_name` from this analyzer

        Args:
            tool_name (str): the name of the tool being removed
        
        Returns:
            bool: true if the tool was removed and false if it was not

        """
        if tool_name in self.__tools.keys():        
            self.__tools.remove(tool_name)
            return True
        return False

    def run_raw(self) -> List[StaticError]:
        """Runs all the tools in this analyzer with their current configurations

        Returns:
            [StaticError]: a list of all the errors reported from running all of 
                the tools in this analyzer

        """
        return self.__run()

    def run_md(self) -> str:
        """Runs all the tools in this analyzer with their current configurations

        Returns:
            str: a formatted markdown string of all of the errors collected
                from this run
                
        """

        errors: List[StaticError] = self.__run()

        #headers will be the header of the created table
        headers = ["Error Type", "Line Number", "Error Description", "Code"]

        #error_markdown is a list of lists where each list represents one error
        #tabulate is used to create the wanted table of multiple errors with description of what and where it occurs in the code
        error_markdown = []
        for error in errors:
            error_markdown.append([error.error_name, error.line_no, error.error_description, error.code])
        if(len(error_markdown) == 0):
            return 'No static errors reported.'
        else:
            return ''.join(tabulate(error_markdown, headers, tablefmt='github'))

    
    def __run(self) -> List[StaticError]:
        errors: List[StaticError] = []
        for name, tool in self.__tools.items():
            errors.extend(tool.run())
        return errors
