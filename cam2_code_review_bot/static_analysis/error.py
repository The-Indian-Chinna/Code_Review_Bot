class StaticError:
    """Data structure class for error report information.
    
    TODO:
        Replace error names with enums. This is to better help data 
            collection metrics

    """

    def __init__(
        self,
        file_path: str = '',
        line_no: int = 1,
        code: str = '',
        error_id: int = 0,
        error_name: str = 'UNKNOWN ERROR',
        error_description: str = 'The error reported is unknown. It has not been defined by OPTIMUS.',
        tool_name: str = 'OPTIMUS',
        is_false_positive: bool = False,
        pull_request: int = 0,
        commit_hash: str = ''
    ):
        self.__file_path = file_path
        self.__line_no = line_no
        self.__code = code
        self.__error_id = error_id
        self.__error_name = error_name
        self.__error_description = error_description
        self.__tool_name = tool_name
        self.__is_false_positive = is_false_positive
        self.__pull_request = pull_request
        self.__commit_hash = commit_hash

    @property
    def file_path(self):
        """str: The path of the file the error is reported in. """
        return self.__file_path

    @property
    def line_no(self):
        """int: The line number the error is reported on. """
        return self.__line_no

    @property
    def code(self):
        """str: The code or (text) on the reported line. """
        return self.__code

    @property
    def error_id(self):
        """int: The numeric ID of the error. """
        return self.__error_id

    @property
    def error_name(self):
        """str: The name of the error, as defined by the tool reporting it."""
        return self.__error_name

    @property
    def error_description(self):
        """str: A detailed definition of the error, as defined by the tool reporting it. """
        return self.__error_description

    @property
    def tool_name(self):
        """str: The name of the tool reporting the error. """
        return self.__tool_name

    @property
    def is_false_positive(self):
        """bool: Flag to denote if this error is a false """
        return self.__is_false_positive

    @property
    def pull_request(self):
        """int: The number of the pull request this error was reported in. """
        return self.__pull_request

    @property
    def commit_hash(self):
        """str: The commit hash this error was reported in. """
        return self.__commit_hash

    def to_md(self) -> str:
        """Converts this error to a md formatted str

        Returns:
            str: the formatted markdown string

        TODO:
            update to better format
        
        """

        md: str = f"{self.error_name} reported on line {self.line_no}: {self.error_description}\n`{self.code}`"

        return md