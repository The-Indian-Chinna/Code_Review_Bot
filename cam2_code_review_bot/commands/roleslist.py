from . import Command, CommandPayload, register_command

roles = ["LOGIC", "CODE FORMAT", "DOC FORMAT"]


async def roleslist(gh, issue_url, comment_url) -> bool:

    # List all of the roles
    body = "\n".join(map(str, roles))

    # Replace the url to say "issues" if "pulls" exists
    issue_url = issue_url.replace("/pulls/", "/issues/")

    await gh.post(
        issue_url + "/comments",
        data={"body": "The following are the allowed roles (case insensitive):\n" + body},
    )
    return True


class RolesListCommand(Command):
    async def call(self, command_payload: CommandPayload) -> bool:
        return await roleslist(
            command_payload.gh, command_payload.issue_url, command_payload.comment_url
        )


register_command("roles", RolesListCommand)
