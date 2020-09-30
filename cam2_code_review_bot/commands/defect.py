import cam2_code_review_bot.dynamodb as dynamodb
import re
from . import Command, CommandPayload, register_command


async def documentationDefect(comment_data, args, issue_url):
    defect_count = dynamodb.getDefectCount()
    defect = dict()
    if len(args) > 8:  # if the input line is multi line
        line_num = [i for i in range(int(args[4]), int(args[6]) + 1)]
        endline_num = -1 - (
            (int(args[6]) + 1) - (int(args[4]) + 1)
        )  # calculate the end of the selected line
        code_seg = [
            (comment_data["diff_hunk"].split("\n")[x])[1:] for x in range(-1, endline_num - 1, -1)
        ]
        code_seg = code_seg[::-1]
        defect.update(
            {
                "defect_number": int(defect_count),
                "file_name": comment_data["path"],
                "description": args[9],
                "line_numbers": line_num,
                "code_segments": code_seg,
            }
        )
    else:
        line_num = [int(args[4])]  # if the input line is a single line
        code_seg = list(comment_data["diff_hunk"].split("\n"))
        defect.update(
            {
                "defect_number": int(defect_count),
                "file_name": comment_data["path"],
                "description": args[7],
                "line_numbers": line_num,
                "code_segments": [code_seg[-1].replace("+", "")],
            }
        )
    dynamodb.createDefect(defect)

    # Update the documentation_defects field in issue
    issue_number = issue_url.split("/")[-1]
    updatedissue = dict()
    currIssue = dynamodb.getIssue(int(issue_number))
    lgic_num = list()
    for item in currIssue["documentation_defects"]:
        lgic_num.append(int(item))
    lgic_num.append(defect["defect_number"])
    updatedissue.update({"documentation_defects": lgic_num})
    dynamodb.updateIssue(int(issue_number), updatedissue)


async def logicDefect(comment_data, args, issue_url):
    defect_count = dynamodb.getDefectCount()
    defect = dict()
    if len(args) > 8:  # if the input line is multi line
        line_num = [i for i in range(int(args[4]), int(args[6]) + 1)]
        endline_num = -1 - (
            (int(args[6]) + 1) - (int(args[4]) + 1)
        )  # calculate the end of the selected line
        code_seg = [
            (comment_data["diff_hunk"].split("\n")[x])[1:] for x in range(-1, endline_num - 1, -1)
        ]
        code_seg = code_seg[::-1]
        defect.update(
            {
                "defect_number": int(defect_count),
                "file_name": comment_data["path"],
                "description": args[9],
                "line_numbers": line_num,
                "code_segments": code_seg,
            }
        )
    else:
        line_num = [int(args[4])]  # if the input line is a single line
        code_seg = list(comment_data["diff_hunk"].split("\n"))
        defect.update(
            {
                "defect_number": int(defect_count),
                "file_name": comment_data["path"],
                "description": args[7],
                "line_numbers": line_num,
                "code_segments": [code_seg[-1].replace("+", "")],
            }
        )
    dynamodb.createDefect(defect)

    # Update the logic defects field in issue
    issue_number = issue_url.split("/")[-1]
    updateissue = dict()
    currIssue = dynamodb.getIssue(int(issue_number))
    lgic_num = list()
    for item in currIssue["logic_defects"]:
        lgic_num.append(int(item))
    lgic_num.append(defect["defect_number"])
    updateissue.update({"logic_defects": lgic_num})
    dynamodb.updateIssue(int(issue_number), updateissue)


class DefectCommand(Command):
    async def call(self, command_payload: CommandPayload) -> bool:
        if command_payload.args[0] == "documentation":
            await documentationDefect(
                command_payload.comment_data, command_payload.args, command_payload.issue_url
            )
            # TODO check if errors need to be reported
            return True
        elif command_payload.args[0] == "logic":
            await logicDefect(
                command_payload.comment_data, command_payload.args, command_payload.issue_url
            )
            # TODO check if errors need to be reported
            return True
        else:
            return False


register_command("report", DefectCommand)
