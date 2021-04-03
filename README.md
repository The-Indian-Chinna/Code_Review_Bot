# CAM2CodeReviewBot (Property of CAM2)
Bot from the CAM2 Software Engineering Team that helps facilitate code review. 

## How to Run the Bot
### Development Tools
The only development tool you will need is python version 3.6 which can be found [here](https://www.python.org/downloads/release/python-360/)

### Cloning the Repo
To start, you can clone the repo by running: 

```
git clone https://github.com/PurdueCAM2Project/CAM2CodeReviewBot.git 
```

Next, navigate to the directory created by the previous command by running:

```
cd CAM2CodeReviewBot
```

### Creating a Virtual Environment
To prevent any system-wide Python dependency issues, use a virtual environment using the Python module [venv](https://docs.python.org/3/tutorial/venv.html). Create the virtual environment in the same folder as the bot's repository by running:

```
python -m venv optimus-env
```

This will create our virtual environment in the working directory.

Our next step is to activate the virtual environment. this command will give us a local python interpreter to run commands like `pip` so we can install our dependencies. **IMPORTANT** this is platform **dependent** so make sure you use the correct command for your OS.

#### Windows (cmd)
```
./optimus-env/Scripts/activate.bat
```

#### Windows (powershell)
```
./optimus-env/Scripts/Activate.ps1
```

### Windows (bash)
```
source ./optimus-env/Scripts/activate
```

#### Unix / Mac OSX
```
source ./optimus-env/bin/activate
```
To validate that this has worked, your terminal prompt should now have `(optimus-env)` appended to the front.

### Installing dependencies
Our bot uses a few python dependencies. We can install them into our virtual environment by running:
```
pip install -r requirements.txt
```

### Running the Bot
After all of the dependencies have been installed, you can run the bot inside the virtual environment by running:
```
python -m cam2-code-review-bot
```

### Exiting the Virtual Environment
To exit out of the interpreter you can run the following command (it is platform independent).
```
deactivate
```

## How to Configure the Bot
Open the file `config.json` and enter the name of the account you want to turn into a code review bot in the `BOTNAME` field and enter its GitHub API Token in the `GITHUBTOKEN` field. The API token can be obtained from [here](https://github.com/settings/tokens).

## Supported Commands
Commands are executed from the GitHub comments section of issues and pull requests.
See more [here](https://github.com/noah-curran/CAM2CodeReviewBot/blob/master/commands/README.md).

> note these libraries are platform specific and may be required for some functionalities on Mac OSX
- `brew tap oclint/formulae`
- `brew install oclint`
- `npm install standard --global`
