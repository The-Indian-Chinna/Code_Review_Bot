import emojis


async def status(gh, issue_url, reviewer):
    """get pull request info"""
    top_comment = await gh.getitem(issue_url)
    pull_body = top_comment["body"]

    """ update top comment """
    if reviewer in pull_body:
        before = emojis.encode(":x:") + " | @" + reviewer
        after = emojis.encode(":white_check_mark:") + " | @" + reviewer
        new_body = pull_body.replace(before, after)
        await gh.patch(issue_url, data={"body": new_body})
