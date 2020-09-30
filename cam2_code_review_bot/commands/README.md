# Command Documentation
The following is a detailed description of the commands that the bot can currently execute and how to use them.

## Commands
##### Table of Contents
[Hello World!](#hello-world)  
[Initialize Issue](#initialize-issue)  
[Assign Reviewers](#assign-reviewer)  
[List Role Types](#list-role-types)  
[Lint Code](#lint-code)  
[Assign Parent Issue](#assign-parent-issue)  
[Open New Issue](#open-new-issue)  
[Report Defect](#report-defect)  
[Show Reviewers](#show-reviewers)  
[Show Issue Dependencies](#show-issue-dependencies)  

**Note: all commands are issued through the GitHub discussion section of an issue. Items within "[" "]" are _optional parameters_.**

## Hello World!
#### Command format:
```
@bot-name hello
```

#### Arguments:  
*None*

## Initialize Issue
#### Command format:
```
@bot-name init
```
OR
```
@bot-name initialize
```

#### Arguments:  
*None*

## Assign Reviewers
#### Command format:
```
@bot-name assign issue to @<GitHub Username> with role <Role> and description "<Description>"
```

#### Arguments:  
*GitHub Username*: The GitHub username of the user you want to assign to the pull request.  
*Role*: The role the user must perform during the code review. See [List Role Types](#list-role-types) for valid roles.  
*Description*: The description of what this code reviewer must do.  

**Note: this command can only be used on a pull request.**  

## List Role Types
#### Command format:
```
@bot-name roles
```
#### Arguments:  
*None*

## Lint Code
#### Command format:
```
@bot-name lint code [of langauge <Code Language>]
```

#### Arguments:  
*Code Language* (optional): The specific language of the code you would like to be linted.  

**Note: this command can only be used on a pull request. You can use "all" in the *Code Language* argument to have the same effect as `@bot-name lint code`.**  

## Assign Parent Issue
#### Command format:
```
@bot-name parent issue is <Issue Number>
```

#### Arguments:  
*Issue Number*: The issue number of the issue you would like to be the parent issue.  

## Open New Issue
#### Command format:
```
@bot-name open issue with title "<Title>" [and description "<Description>"]
```

#### Arguments:  
*Title*: The title the new issue will have.  
*Description* (optional): The description given to the new issue. This will display in the body of the issue.  

## Report Defect
#### Command format:
```
@bot-name report [documentation|logic] defect from lines <Starting Line Number> to <Ending Line Number> with description "<Description>"
```
OR
```
@bot-name report [documentation|logic] defect on line <Line Number> with description "<Description>"
```

#### Arguments:  
*Starting Line Number*: For multi-line defects, this is the line the defect starts on.
*Ending Line Number*: For multi-line defects, this is the line the defect ends on.
*Line Number*: For single-line defects, this is the line the defect occurs on.
*Description*: A short description of the defect.

**Note: "documentation" or "logic" can be chosen. Whichever one you choose should resemble the kind of defect. In the backend, it will be stored separately for sake of organization.

## Show Reviewers
#### Command format:
```
@bot-name show reviewers
```
#### Arguments:  
*None*

## Show Issue Dependencies
#### Command format:
```
@bot-name show issue dependencies
```
#### Arguments:  
*None*

## Adding New Commands
The commands API is self contained so when creating a command you only need to edit 2 files, `init.py` and `{new_command}.py`, where "new_command" is the name of your command. To add a new command there are 3 steps:
- [Define](#Defining-a-New-Command)
- [Register](#Registering-a-New-Command)
- [Import](#Importing-a-New-Command)

> Note: All files related to commands should be in the `commands` directory. 

### Defining a New Command
All commands are subclasses of the base class `Command`. This is an abstract class with 1 abstract method `call`. This method takes in a single argument `CommandPayload`, a struct with all the data your command will be able to access at runtime. 

#### File Structure
All commands have a similar file structure as shown here.
```python
# commands/example_command.py

# these are developer dependencies for building your command. 
from commands import Command, CommandPayload, register_command

# additional imports ...

# Define the new command class. Note the inheritance from Command
def class ExampleCommand(Command):
    """This docstring is where you should document your command 
    """

    # Note: this method dshould not have a docstring
    async def call(self, payload: CommandPayload) -> bool:
        # implement your command here ...
        print ('this is my example command')
        return True

# register the command here. This adds it to Optimus
register_command('example', ExampleCommand())
```


#### The `call` Method
This method is where you can define the functionality of your command. It is the only place where you should have to write code. Remember your command is stateless, so the scope of this method is also the scope of this command.

Example: 

```python
async def call(self, payload: CommandPayload) -> bool: 
    # implement your command here ...
    print ('this is my example command')
    return True
```

> Note: the `call` method is asynchronous because it is triggered from a webhook

### Registering a New Command
The command developer API will manage your command. This means rather than editing a webhook or endpoint all you have to do is register the command in the command registry. To do this after defining your command call the `register_command` method with your commands name and a new instance. 

Example:
```python
# this will register your command under the name 'example'.
register_command('example', ExampleCommand)  
```

The name you provide here is how the command will be called. So the above example would be called by `@optimus example` where `optimus` is the name of the bot and `example` is the name of the command.


> Note: if you try to register the name of an existing command then this will raise a ValueError

### Importing a New Command
After defining and registering your command it needs to be imported to the `__init__.py` file in the `commands` directory. This is so when optimus is built and run your command will be registered. 

```python
# commands/__init__.py

# These are command developer dependencies
from .command_payload import CommandPayload
from .command import Command
from .command_registry import register_command, is_registered_command, get_command

# other command imports ...

# You can import your command at the bottom of the file
from . import example_command 
```