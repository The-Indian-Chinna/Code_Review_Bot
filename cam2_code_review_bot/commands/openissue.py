import sys

sys.path.append("..")

import cam2_code_review_bot.dynamodb as dynamodb
from . import Command, CommandPayload, register_command


async def openissue(gh, issue_url, repo_url, args) -> True:
    """
    args:
        arg[3] is the title of the new issue
        arg[6] is the body of the new issue (optional)
    """

    # If the proper arguments aren't passed through, don't compute and notify the user
    if len(args) < 4:
        # Replace the url to say "issues" if "pulls" exists
        issue_url = issue_url.replace("/pulls/", "/issues/")

        await gh.post(
            issue_url + "/comments",
            data={
                "body": 'Command failed. Please use format `@bot-name open issue with title "<title of new issue>" [and description "<body of new issue>"]`.'
            },
        )
        return False

    # Get the issue number and its associated database info
    curr_issue_number = int(issue_url[issue_url.rindex("/") + 1 :])
    issue_db_info = dynamodb.getIssue(curr_issue_number)

    # Do nothing if the current issue is not initialized in the database.
    # Notify the user that they must initialize the current issue.
    if issue_db_info is None:
        # Replace the url to say "issues" if "pulls" exists
        issue_url = issue_url.replace("/pulls/", "/issues/")

        await gh.post(
            issue_url + "/comments",
            data={
                "body": "Command failed. Please first initialize the repository by using `@bot-name init` and then try again."
            },
        )
        return False

    # The second argument, the description of the issue, is optional.
    # Add a dummy argument if it does not exist.
    if len(args) < 5:
        body = ""
    else:
        body = args[6]

    # Create the new issue
    child_issue = await gh.post(repo_url + "/issues", data={"title": args[3], "body": body})

    # Add the new issue to the database (and essentially initializing it)
    child_issue_db_info = {
        "issue_number": int(child_issue["number"]),
        "reviewers": [],
        "changed_files": [],
        "parent_issue": curr_issue_number,
        "child_issues": [],
        "documentation_defects": [],
        "logic_defects": [],
    }
    dynamodb.createIssue(child_issue_db_info)

    await gh.post(
        child_issue["url"] + "/comments", data={"body": "🤖 The bot has initialized this issue!"},
    )

    # Add the new issue to the parent issue's database entry
    issue_db_info["child_issues"].append(child_issue["number"])
    changed_db_info = {"child_issues": issue_db_info["child_issues"]}
    dynamodb.updateIssue(curr_issue_number, changed_db_info)

    # Replace the url to say "issues" if "pulls" exists
    issue_url = issue_url.replace("/pulls/", "/issues/")

    await gh.post(
        issue_url + "/comments",
        data={
            "body": "New issue has been successfully created as #"
            + str(child_issue["number"])
            + "."
        },
    )

    return True


class OpenIssueCommand(Command):
    async def call(self, command_payload: CommandPayload) -> bool:
        return await openissue(
            command_payload.gh,
            command_payload.issue_url,
            command_payload.repo_url,
            command_payload.args,
        )


register_command("open", OpenIssueCommand)
