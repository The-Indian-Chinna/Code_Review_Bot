import cam2_code_review_bot.dynamodb as dynamodb
import emojis

from . import Command, CommandPayload, register_command

roles = ["LOGIC", "CODE FORMAT", "DOC FORMAT"]


async def assign(gh, issue_url, comment_url, args) -> bool:

    # If not a pull request, you cannot assign a reviewer
    if "/issues/" in issue_url:
        # Replace the url to say "issues" if "pulls" exists
        issue_url = issue_url.replace("/pulls/", "/issues/")

        await gh.post(
            issue_url + "/comments",
            data={
                "body": "Command failed. You cannot assign code reviewers to an issue. You can only assign reviewers to pull requests."
            },
        )
        return False

    # If the proper arguments aren't passed through, don't compute and notify the user
    if len(args) < 3:
        # Replace the url to say "issues" if "pulls" exists
        issue_url = issue_url.replace("/pulls/", "/issues/")

        await gh.post(
            issue_url + "/comments",
            data={
                "body": 'Command failed. Please use format `@bot-name assign issue to @user-name with role <role> and description "<description of role>"`.'
            },
        )
        return False

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

    reviewer = args[2][1:]
    role = args[5]
    description = args[8]

    reviewers = issue_db_info["reviewers"]
    reviewers.append(reviewer)
    if role.upper() not in roles:
        # Replace the url to say "issues" if "pulls" exists
        issue_url = issue_url.replace("/pulls/", "/issues/")

        await gh.post(
            issue_url + "/comments",
            data={
                "body": "Command failed. Provided role does not exist. Use the command `@bot-name roles` to see existing roles."
            },
        )
        return False

    """
    The following is how to tell if the message is in the conversation tab or in a file change tab
    """

    # comment_id = comment_url[comment_url.rfind('/') + 1:]
    # parent_comment = issue_url + '/comments/' + comment_id + '/replies'

    # ''' "pulls" in comment_url when commented in file change tab
    # 	"issues" in comment_url when commented in conversation tab, but "pulls" in issue_url'''
    # if "/pulls/" in comment_url:
    # 	await gh.post(parent_comment, data={
    # 		'body': body
    # 	})
    # elif "/issues/" in comment_url:
    # 	new_issue_url = issue_url.replace("/pulls/", "/issues/")
    # 	await gh.post(new_issue_url + '/comments', data={
    # 		'body': body
    # 	})

    # Create an entry for the reviewer information in the database
    dynamodb.createReviewer(
        {
            "github_username": reviewer,
            "issue_number": issue_number,
            "role": role,
            "role_description": description,
        }
    )

    # Update the entry for the issue in the database to include the new reviewer
    issue_db_info["reviewers"] = reviewers
    dynamodb.updateIssue(issue_number, issue_db_info)

    # Request the new reviewer
    await gh.post(issue_url + "/requested_reviewers", data={"reviewers": reviewers})

    # Replace the url to say "issues" if "pulls" exists
    issue_url = issue_url.replace("/pulls/", "/issues/")

    await gh.post(
        issue_url + "/comments", data={"body": "@" + reviewer + " is successfully assigned!"},
    )
    return True


class AssignCommand(Command):
    async def call(self, command_payload: CommandPayload) -> bool:
        return await assign(
            command_payload.gh,
            command_payload.issue_url,
            command_payload.comment_url,
            command_payload.args,
        )


register_command("assign", AssignCommand)
