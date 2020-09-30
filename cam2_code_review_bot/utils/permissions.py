async def is_admin(gh, repo_url, username):
    # Obtain the permission url of form /repos/:owner/:repo/collaborators/:username/permission
    permission_url = repo_url + "/collaborators/" + username + "/permission"

    # Get the permission info from the GitHub API
    permission_info = await gh.getitem(permission_url)

    # Get the permission level
    # Can be one of: admin, write, read, none
    permission = permission_info["permission"]

    return permission == "admin"


async def is_requester(gh, issue_url, username):
    # Get the issue info from the GitHub API
    issue_info = await gh.getitem(issue_url)

    # Get the user who made the issue/pull request
    issue_user = issue_info["user"]["login"]

    return issue_user == username
