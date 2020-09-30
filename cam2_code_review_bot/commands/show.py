import cam2_code_review_bot.dynamodb as dynamodb
from . import Command, CommandPayload, register_command


async def showreviewers(gh, issue_url) -> bool:

    # Get the issue number and its associated database info
    issue_number = int(issue_url[issue_url.rindex("/") + 1 :])
    issue_db_info = dynamodb.getIssue(issue_number)

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

    # Obtain information for reviewers in this pull request.
    reviewers = []
    for reviewer in issue_db_info["reviewers"]:
        reviewer_db_info = dynamodb.getReviewer(reviewer, issue_number)
        reviewers.append(reviewer_db_info)

    # Format reviewer information into a Markdown table.
    reviewer_info = "\n\nUsername | Role | Description\n--- | --- | ---"
    for reviewer in reviewers:
        reviewer_info = (
            reviewer_info
            + "\n"
            + reviewer["github_username"]
            + " | "
            + reviewer["role"]
            + " | "
            + reviewer["role_description"]
        )

    # Replace the url to say "issues" if "pulls" exists
    issue_url = issue_url.replace("/pulls/", "/issues/")

    await gh.post(
        issue_url + "/comments",
        data={
            "body": "These are the reviewers for this issue along with their role and a description for their role:"
            + reviewer_info
        },
    )
    return True


async def showissuedependencies(gh, issue_url) -> bool:

    # Get the issue number and its associated database info
    issue_number = int(issue_url[issue_url.rindex("/") + 1 :])
    issue_db_info = dynamodb.getIssue(issue_number)

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

    # Format parent issue.
    if issue_db_info["parent_issue"] > 0:
        parent_issue_info = "**Parent Issue:** #" + str(issue_db_info["parent_issue"])
    else:
        parent_issue_info = "**Parent Issue:** None."

    # Format child issues.
    child_issue_info = "**Child Issues:**"
    if len(issue_db_info["child_issues"]) > 0:
        is_first = True
        for child_issue in issue_db_info["child_issues"]:
            if not is_first:
                child_issue_info = child_issue_info + ","
            else:
                is_first = False

            child_issue_info = child_issue_info + " #" + str(child_issue)
    else:
        child_issue_info = child_issue_info + " None."

    # Replace the url to say "issues" if "pulls" exists
    issue_url = issue_url.replace("/pulls/", "/issues/")

    await gh.post(
        issue_url + "/comments",
        data={
            "body": "These are the issue dependencies for this issue:\n\n"
            + parent_issue_info
            + "\n\n"
            + child_issue_info
        },
    )
    return True


class ShowCommand(Command):
    async def call(self, command_payload: CommandPayload) -> bool:
        if command_payload.args[0] == "reviewers":
            return await showreviewers(command_payload.gh, command_payload.issue_url)
        elif command_payload.args[0] == "issue":
            return await showissuedependencies(command_payload.gh, command_payload.issue_url)
        else:
            return False


register_command("show", ShowCommand)
