import sys

sys.path.append("..")

import cam2_code_review_bot.dynamodb as dynamodb
from . import Command, CommandPayload, register_command


async def parentissue(gh, issue_url, repo_url, args):
    """
    args:
        arg[2] is the issue number of the parent issue
    """

    if len(args) < 3:
        # Replace the url to say "issues" if "pulls" exists
        issue_url = issue_url.replace("/pulls/", "/issues/")

        await gh.post(
            issue_url + "/comments",
            data={
                "body": "Command failed. Please use format `@bot-name parent issue is <parent issue number>`."
            },
        )
        return

    if not args[2].isdigit() or int(args[2]) == 0:
        # Replace the url to say "issues" if "pulls" exists
        issue_url = issue_url.replace("/pulls/", "/issues/")

        await gh.post(
            issue_url + "/comments",
            data={
                "body": "Command failed. Please use a positive integer value as input with the format `@bot-name parent issue is <parent issue number>`."
            },
        )
        return

    # Obtain the current issue data and obtain where the old parent issue location is in the main post.
    issue_data = await gh.getitem(issue_url)

    # Make sure the child issue is in the database.
    issue_db_info = dynamodb.getIssue(issue_data["number"])
    if issue_db_info is None:
        # Replace the url to say "issues" if "pulls" exists
        issue_url = issue_url.replace("/pulls/", "/issues/")

        await gh.post(
            issue_url + "/comments",
            data={
                "body": "Command failed. Please first initialize this repository by using `@bot-name init` and then try again."
            },
        )
        return

    # Make sure the new parent issue is in the database.
    new_parent_issue_db_info = dynamodb.getIssue(int(args[2]))
    if new_parent_issue_db_info is None:
        # Replace the url to say "issues" if "pulls" exists
        issue_url = issue_url.replace("/pulls/", "/issues/")

        await gh.post(
            issue_url + "/comments",
            data={
                "body": "Command failed. Please first initialize the parent repository by using `@bot-name init` in #"
                + args[2]
                + " and then try again."
            },
        )
        return

    # Obtain the old parent issue's number
    old_parent_issue_number = issue_db_info["parent_issue"]

    # If there is no old parent issue, old_parent_issue_number will be -1
    if old_parent_issue_number > 0:
        # Remove child issue from old parent issue.
        # The database entry should already exist.
        old_parent_issue_db_info = dynamodb.getIssue(old_parent_issue_number)
        old_parent_issue_db_info["child_issues"].remove(issue_data["number"])
        dynamodb.updateIssue(old_parent_issue_number, old_parent_issue_db_info)

    # Add child issue to new parent issue.
    new_parent_issue_db_info["child_issues"].append(issue_data["number"])
    dynamodb.updateIssue(int(args[2]), new_parent_issue_db_info)

    # Add new parent issue to child issue.
    issue_db_info["parent_issue"] = int(args[2])
    dynamodb.updateIssue(issue_data["number"], issue_db_info)

    # Replace the url to say "issues" if "pulls" exists
    issue_url = issue_url.replace("/pulls/", "/issues/")

    await gh.post(
        issue_url + "/comments",
        data={"body": "The parent issue has been successfully changed to #" + args[2] + "."},
    )
    return


class ParentIssueCommand(Command):
    async def call(self, command_payload: CommandPayload) -> bool:
        return await parentissue(
            command_payload.gh,
            command_payload.issue_url,
            command_payload.repo_url,
            command_payload.args,
        )


register_command("parent", ParentIssueCommand)
