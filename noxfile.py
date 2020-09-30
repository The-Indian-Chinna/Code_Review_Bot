import nox

FILEPATHS = [
    "noxfile.py",
    "cam2_code_review_bot/dynamodb",
    "cam2_code_review_bot/commands",
    "cam2_code_review_bot/cam2_code_review_bot.py",
    "cam2_code_review_bot/utils",
    "tests",
    "setup.py",
]


@nox.session(python="3.7")
def tests(session):
    session.run("pip", "install", "-e", ".")
    session.run("pip", "install", "-r", "requirements.txt")
    session.install("pytest", "pytest-asyncio")
    session.run("pytest")


@nox.session(python="3.7")
def lint(session):
    session.install("black")
    session.run("black", "--check", "--line-length", "100", *FILEPATHS)


@nox.session(python="3.7")
def reformat(session):
    session.install("black")
    session.run("black", "--line-length", "100", *FILEPATHS)
