# Static Analysis

## Usage
All the functionality for this module can be accessed through the `StaticAnalyzer` class. This class allows the developer to add, configure and run a given set of tools. 

Example:
```python
from static_analysis import StaticAnalyzer

def static_reporter() -> None:
    # Create a new static analyzer object
    static_analyzer: StaticAnalyzer = StaticAnalyzer()
    
    # Add tools to the analyzer
    static_analyzer.add_tool(ExampleTool())

    # Configure the added tools. 'example-tool' is the name of 
    # the tool being configured and 'config.json' is the 
    # configuration file.
    static_analyzer.configure_tool_from_file('example-tool', 'config.json')

    # This runs all the tools in the analyzer and returns an error 
    # report formatted with markdown.
    formatted_report: str = static_analyzer.run_md()

```

## Creating an Error
Static analysis in Optimus uses a generic error format `StaticError`. This is a base struct that contains information about an error such as the `error_name`, `file_path`, `line_no` etc. All static analysis tools in Optimus will return a list of `StaticError`. The following example shows how you can fill out this struct.

Example:
```python
from static_analysis import StaticError

def create_error() -> StaticError:
    # the following creates an error with some basic 
    # error information. see (static_analysis/error.py 
    # for more information)
    static_error: StaticError = StaticError(
        file_path='path/to/file',
        line_no=5,
        code='bad.func()',
        error_name='IMPORT ERROR',
        error_description = '"bad" is not imported.',
        tool_name = 'OPTIMUS',
        is_false_positive = False
    )

    return static_error

```

## Defining a New Error
The static analysis API also allows for developers to create predefined errors. This is done by extending the `StaticError` class and passing static values to some parameters. All new defined errors should be defined in `static_analysis/errors/error_name.py` where error name is the name of the new error.

Example:
```python
from static_analysis import StaticError

class ExampleError(StaticError):

    def __init__(self, file_path: str, line_no: int, code: str):
        # Note the use of the super constructor, and hardcoding 
        # of some parameters uniform to all errors of this type
        super.__init__(
            self, 
            file_path=file_path,
            line_no=line_no,
            code=code,
            error_name='example',
            error_description='example error description',
            tool_name='example-tool',
            is_false_positive=False    
        )

```

The above example defines a new error `ExampleError` allowing to reduce the parameters needed to create an error. This allows us to change our `create_error` from above if we know the specific type of error.

```python
from static_analysis.errors import ExampleError

def create_example_error():
    example_error: ExampleError = ExampleError(
        file_path='path/to/file',
        line_no=5,
        code='bad.func()'
    )

    return example_error

```

## Adding a New Tool
This module provides an API for defining a new tool. All tools must be subclasses of the abstract class `StaticTool`. Each tool must implement 2 abstract methods to work properly, `load_config` and `run`. In addition to that each tool should define a `JSON` configuration file. Finally each tool must define a name for itself.  

> Note all tools are defined in the folder `static_analysis/tools/`

### Defining a Name
A tool has its name defined in the constructor. For ease of use, we recommend you give your tool a static name and do not expose it as a parameter. 

Example:
```python
# example_tool.py

from static_analysis import StaticTool

class ExampleTool(StaticTool):
    """All tools should include a docstring.

    This docstring should include the following:
        * the tools name
        * what the tool does when `run` is called
        * how the configuration file is defined (`load_config`)

    """

    # Your tool must define a constructor to set the name 
    def __init__(self):
        # Note the use of a static name corresponding to the 
        # class name. 
        super.__init__(self, 'example-tool')

```

### Implementing `load_config`
This method is how you can set the state of your tool. All tools are configured from `JSON` files or objects, however it is up to this method's implementation on how that configuration is stored and accessed later.

Example:
```python
def load_config(self, config: json) -> None:
    # Read in a configuration parameters from the `config` object passed
    self.__example_config_one = config['config-one']
    self.__example_config_two = config['config-two']

```

### Implementing `run`
This method will run your tool with the configurations defined by `load_config`. This can be done through the cli and a third-party tool or through the use of another module. After executing it should return a `List[StaticError]`. If no errors are found you should return an empty list. The example below shows how you might define this method to work with a tool run on the command line.

Example:

```python
def run(self) -> List[StaticError]:
    # Code to setup and get input omitted ...

    # This is example code to run a command on the shell.
    process = subprocess.Popen(
        'example-tool-cli ' + self.__example_config_one, 
        shell=True, 
        stdout=subprocess.PIPE
    )
    stdout, _ = process.communicate()
    output: str = stdout.decode('{file encoding}')

    # Convert output to error. This step has been simplified 
    # for this example.
    error: StaticError = StaticError(output)

    # Close the process
    process.stdout.close()

    # Return the final result as a List. 
    # Note: this is not restricted to just a single error.  
    return [error]

```
### Full Example
The 3 previous sections combined into a complete example.

```python 
# example_tool.py
import json
import subprocess
from static_analysis import StaticTool, StaticError

class ExampleTool(StaticTool):
    """All tools should include a docstring.

    This docstring should include the following:
        * the tools name
        * what the tool does when `run` is called
        * how the configuration file is defined

    """

    # Your tool must define a constructor to set the name 
    def __init__(self):
        # Note the use of a static name corresponding to the class name. 

        # Initialize member variables
        self.__example_config_one = ''
        self.__example_config_two = 0

        # Call base constructor
        super.__init__(self, 'example-tool')

    def load_config(self, config: json) -> None:
        # Read in a configuration parameters from the `config` object passed
        self.__example_config_one = config['config-one']
        self.__example_config_two = config['config-two']

    def run(self) -> List[StaticError]:
        # This is example code to run a command on the shell.
        process = subprocess.Popen(
            'example-tool-cli', 
            shell=True, 
            stdout=subprocess.PIPE
        )
        stdout, _ = process.communicate()
        output: str = stdout.decode('{file encoding}')

        # Convert output to error. This step has been simplified 
        # for this example.
        error: StaticError = StaticError(output)

        # Close the process
        process.stdout.close()

        # Return the final result as a List. 
        # Note: this is not restricted to just a single error.  
        return [error]

```

> Note: This example does not *work* and its purpose is to demonstrate the structure of a tool. 