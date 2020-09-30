from . import Command, CommandPayload, register_command


async def hello(gh, issue_url):
    issue_url = issue_url.replace("/pulls/", "/issues/")
    resp = await gh.post(issue_url + "/comments", data={"body": "Hello human!"})
    return resp


class HelloCommand(Command):
    async def call(self, command_payload: CommandPayload) -> bool:
        response = await hello(command_payload.gh, command_payload.issue_url)
        # TODO process response here
        return True


register_command("hello", HelloCommand)
