import json
import subprocess
import re
from typing import List, Dict, Any
from . import StaticError, StaticTool

class PerformanceProfilerTool(StaticTool):
    """Implements the cProfile module using the StaticTool interface.

    cProfile is a built-in performance profiler for python code designed to detect performance 
    vunerabilities within a codebase

    the name used to identify this tool is: "performance-profiler"

    """

    file_path: str = ''
    number_of_calls_thresh: int = 0
    cumulative_time_thresh: float = 0.0

    def __init__(self):
        super(PerformanceProfilerTool, self).__init__("performance-profiler")
        
    def load_config(self, config: Dict[str, Any]) -> None:
        """Loads the specified ``configs`` for PerformanceProfiler

        Note:
            only one of or both of the fields `number_of_calls_thresh` or `cumulative_time_thresh`
            can be present in the config file. If a config is excluded then it is ignored when the 
            profiler is run. 

        Configs:
            file_path (str): The relative path to the file to run the profiler on. This must be a
                ".py" file
            number_of_calls_thresh (int): the minimum number of calls needed to classify a piece 
                of code as a performance error. This must be a postive value, negative values are
                ignored.
            cumulative_time_thresh (float): the minimum amount of execution time in seconds needed
                to classify a piece of code as a performance error. This must be a postive value, 
                negative values are ignored.

        Args:
            config (Dict[str, Any]): Configs for performance profiler, (see above)

        Raises:
            ValueError: If "file_path" config is not included in the config file
            ValueError: If "file_path" config is not a python file (".py" extension)
            ValueError: If "number_of_calls_thresh" and "cumulative_time_thresh" are not included
                in the config file.
        """

        if not "file_path" in config:
            raise ValueError('Invalid config file. [file_type] not defined.')

        self.file_path = config['file_path']

        if not '.py' in self.file_path:
            raise ValueError('Invalid file type provided. File must have the extension ".py"')

        if not "number_of_calls_thresh" in config and not "cumulative_time_thresh" in config:
            raise ValueError('Invalid config file. [number_of_calls_thresh] or \
                [cumulative_time_thresh] must be defined.')

        if "number_of_calls_thresh" in config:
            self.number_of_calls_thresh = config['number_of_calls_thresh']
        
        if "cumulative_time_thresh" in config:
            self.cumulative_time_thresh = config['cumulative_time_thresh']

    def run(self) -> List[StaticError]:
        """Runs cProfile with the given configs set by `load_config`

        Returns:
            List[StaticError]: a list of all performance errors reported by cProfile

        """
        error_list = []
        # this is run via the subshell so it can be executed on an entire python file.
        process = subprocess.Popen(
            "python -m cProfile " + self.file_path, shell=True, stdout=subprocess.PIPE
        )
        stdout, _ = process.communicate()

        for output_encoded in stdout.splitlines():

            # the output from stdouy is a byte array so it must be decoded
            output: str = output_encoded.decode()
            
            # this selects only lines that contain a full data entry to a python file from the
            # output from provided by the profiler. If this regex is not matched then either, 
            # 1. the output is not a direct result of source code being reviewed and is irrelevant
            # 2. the output is missing a statistic that is needed for the report.
            match = re.search(r'(\d+(\/|\.)?(\d*))\s+(\d+(\/|\.)?(\d*))\s+(\d+(\/| |\.)?(\d*))\s+(\d+(\/| |\.)?(\d*))\s+(\d+(\/| |\.)?(\d*)) \w*\.py:\d+\(\w+\)', output)
            if match == None:
                # match was not found, skip this entry
                continue

            number_of_calls: int = int(match.group(1))
            cumulative_time: float = float(re.findall(r'\d+\.\d+', match.group(0))[2])

            location: str = re.findall(r'\w+\.py', match.group(0))[0]
            line_number: int = int(re.findall(r':\d+', match.group(0))[0][1:])
            function: str = re.findall(r'\(\w+\)', match.group(0))[0][1:-1]
            
            if not self.file_path.endswith(location):
                # not the file being tested, skip this entry
                continue

            # check the number of calls, skip if not defined in config
            if number_of_calls >= self.number_of_calls_thresh and self.number_of_calls_thresh >= 0:
                static_error: StaticError = StaticError(
                    file_path=self.file_path,
                    line_no=line_number,
                    code=function,
                    error_name='number of calls error',
                    error_description='exceeded the threshhold for maximum number of function calls',
                    tool_name='Performance Profiler'
                )
                error_list.append(static_error)

            # check the cumulative execution time, skip is not defined in config
            if cumulative_time >= self.cumulative_time_thresh and self.cumulative_time_thresh >= 0.0:
                static_error: StaticError = StaticError(
                    file_path=self.file_path,
                    line_no=line_number,
                    code=function,
                    error_name='execution time error',
                    error_description='exceeded the threshhold for maximum execution time',
                    tool_name='Performance Profiler'
                )
                error_list.append(static_error)

        return error_list
