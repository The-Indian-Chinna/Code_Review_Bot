import sys

sys.path.append("..")

import cam2_code_review_bot.dynamodb as dynamodb
import re
from . import Command, CommandPayload, register_command


async def init(gh, issue_url):

    # Obtain the issue information from GitHub
    issue = await gh.getitem(issue_url)

    # Check if this issue has been initialized in the database already
    issue_db_data = dynamodb.getIssue(int(issue["number"]))
    if issue_db_data is not None:
        # Replace the url to say "issues" if "pulls" exists
        issue_url = issue_url.replace("/pulls/", "/issues/")

        await gh.post(
            issue_url + "/comments",
            data={"body": "Command failed. This issue has already been initialized."},
        )
        return

    # Give the issue an entry in the database
    dynamodb.createIssue(
        {
            "issue_number": issue["number"],
            "reviewers": [],
            "changed_files": [],
            "parent_issue": -1,
            "child_issues": [],
            "documentation_defects": [],
            "logic_defects": [],
        }
    )

    # Replace the url to say "issues" if "pulls" exists
    issue_url = issue_url.replace("/pulls/", "/issues/")

    # Confirm to the user that the bot has been successfully initialized
    await gh.post(issue_url + "/comments", data={"body": "🤖 The bot has initialized this issue!"})


class InitCommand(Command):
    async def call(self, command_payload: CommandPayload) -> bool:
        response = await init(command_payload.gh, command_payload.issue_url)
        # TODO process response here
        return True


register_command("init", InitCommand)
