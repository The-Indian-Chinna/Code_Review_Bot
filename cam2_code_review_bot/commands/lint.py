import asyncio
import os
import aiohttp
import subprocess
import requests
import shutil

from . import Command, CommandPayload, register_command

# Supported file extensions and linting commands
extensions = {"python": ".py", "java": ".java", "javascript": ".js", "c": ".c"}
lint_command = {
    "python": "pycodestyle",
    "java": "java -jar 3rdparty/checkstyle-8.26-all.jar -c 3rdparty/sun_checks.xml",
    "javascript": "standard",
    "c": "oclint",
}
lint_args = {"python": "", "java": "", "javascript": "", "c": "-- -c"}

languages = ["python", "java", "javascript", "c"]


async def lint(gh, issue_url, args) -> bool:

    # If not a pull request, you cannot assign a reviewer
    if "/issues/" in issue_url:
        # Replace the url to say "issues" if "pulls" exists
        issue_url = issue_url.replace("/pulls/", "/issues/")

        await gh.post(
            issue_url + "/comments",
            data={
                "body": "Command failed. You cannot lint an issue, as there is no code to lint. You can only lint pull requests."
            },
        )
        return False

    # If the proper arguments aren't passed through, don't compute and notify the user
    if len(args) < 1:
        # Replace the url to say "issues" if "pulls" exists
        issue_url = issue_url.replace("/pulls/", "/issues/")

        await gh.post(
            issue_url + "/comments",
            data={
                "body": "Command failed. Please use format `@bot-name lint code [of langauge <Code Language>]`."
            },
        )
        return False

    # Determine the language to be linted.
    if len(args) < 4:
        language = "all"
    else:
        language = args[3]

    # Make sure the language is allowed.
    if language.lower() != "all" and language.lower() not in languages:
        # Replace the url to say "issues" if "pulls" exists
        issue_url = issue_url.replace("/pulls/", "/issues/")

        await gh.post(
            issue_url + "/comments",
            data={"body": "Command failed. Please use a supported language."},
        )
        return False

    # Get the committed files in the pull request
    committed_files = await gh.getitem(issue_url + "/files")

    # Make temporary directory
    os.mkdir("commands/temp")

    # TODO: Allow all languages to lint at once.
    if language == "all":
        pass
    else:
        # Loop through each file in pull request
        for file in committed_files:
            file_path = file["filename"]

            if file_path.endswith(extensions.get(language)):
                file_data = await gh.getitem(file["contents_url"])
                # Retrieve the commit hash
                file_commit_id = file["contents_url"][file["contents_url"].rfind("=") + 1 :]

                # Obtain the file's code
                r = requests.request("GET", file_data["download_url"])

                file_name = file_data["name"]

                # Create a temporary local file containing the downloaded code
                with open("commands/temp/" + file_name, "w+", encoding=r.encoding) as file_to_check:
                    file_to_check.write(r.text)

                # Execute pycodestyle linting
                cmd = f"{lint_command.get(language)} commands/temp/{file_name} {lint_args.get(language)}"
                proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                stdout, _ = proc.communicate()

                # Assemble bulleted list of linting messages, linking the error found to its respective line number.
                linting_messages = ""
                for line in stdout.decode(r.encoding).splitlines():
                    if line.find(":") != -1:
                        msg = line
                        line_info = msg[line.find(":") + 1 :]
                        number = line_info[: line_info.find(":")]
                        line_url = file_data["html_url"] + "#L" + number
                        print_msg = "\u2022 [Line " + line_info + "](" + line_url + ")"
                        linting_messages = linting_messages + "\n" + print_msg
                proc.stdout.close()

                # If there are no linting errors
                if linting_messages == "":
                    linting_messages = "No linting errors."

                # Post a comment on each file with the linting feedback
                await gh.post(
                    issue_url + "/comments",
                    data={
                        "commit_id": file_commit_id,
                        "path": file_path,
                        "side": "LEFT",
                        "position": 1,
                        "body": linting_messages,
                    },
                )

    # Remove temporary local files
    shutil.rmtree("commands/temp")

    # Indicate the linting has been finished successfully
    await gh.post(
        issue_url + "/reviews",
        data={
            "body": "Linting has been performed. Please review the comment for each file.",
            "event": "REQUEST_CHANGES",
        },
    )

    return True


class LintCommand(Command):
    async def call(self, command_payload: CommandPayload) -> bool:
        return await lint(command_payload.gh, command_payload.issue_url, command_payload.args)


register_command("lint", LintCommand)
