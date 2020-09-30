import asyncio
import os
import json
import threading
import logging

import aiohttp
from quart import Quart, request, jsonify, render_template, send_from_directory
import quart
from gidgethub.aiohttp import GitHubAPI
from typing import Dict, Any

import cam2_code_review_bot.commands as commands
import cam2_code_review_bot.utils as utils
import cam2_code_review_bot.dynamodb as dynamodb

from cam2_code_review_bot.commands import (
    is_registered_command,
    get_command,
    CommandPayload,
    Command,
)

app = Quart(__name__)

# Establishes a lock to force sections of code to function synchronously
key_lock = threading.Lock()


@app.before_serving
async def create_session() -> None:
    """The function that is run prior to the Quart server being started up.
    Gets the following;
        * Github OAUTH Token
        * bot's name
        * aiohttp session
        * gidgethub object
    
    Initalizes the following in DynamoDB:
        * Defects table
        * Issues table
        * Reviewers table
        * Entry count table

    Returns:
        None
    """
    github_oauth_token = os.getenv("GITHUBTOKEN")
    app.bot_name = os.getenv("BOT_NAME")
    app.session = aiohttp.ClientSession()
    app.gh = None

    with key_lock:
        dynamodb.createDefectsTable()
        dynamodb.createIssuesTable()
        dynamodb.createReviewersTable()
        dynamodb.createEntryCountTable()


@app.after_serving
async def destroy_session() -> None:
    """Closes down aiohttp session properly.

    Returns:
        None
    """
    await app.session.close()


@app.route("/", methods=["GET"])
async def index() -> quart.Response:
    """A test function.

    Returns:
        quart.Response
        Returns a Response with a status code of `200 OK`
    """

    return jsonify(success=True)


@app.route("/webhook", methods=["POST"])
async def webhook() -> quart.Response:
    """The main processing functions. Processes things that happen in PR feedback comments and issue/PR comments.
    
    See the following link for documentation:
    https://github.com/PurdueCAM2Project/CAM2CodeReviewBot/tree/master/commands
    
    Returns:
        quart.Response
        A Flask response object to let Github the request was received.
    """
    payload = await request.get_json()
    if "issue" in payload.keys() and payload["action"] == "created":
        comment_text = r["comment"]["body"]
        if comment_text[: len(app.bot_name)] == app.bot_name:
            issue_url = payload["issue"]["url"]
            command, args = utils.extract_command_and_args(comment_text[(len(app.bot_name) + 1) :])

            comment_url: str = ""
            repo_url: str = "/repos/" + payload["repository"]["full_name"]
            comment_data: Dict[str, Any] = {}

            async with aiohttp.ClientSession() as session:
                gh = GitHubAPI(session, app.bot_name, oauth_token=os.getenv("GITHUBTOKEN"))
                utils.Github.initialize(gh)
                command_payload: CommandPayload(
                    gh,
                    issue_url,
                    comment_url,  # NOTE: mocked
                    repo_url,  
                    comment_data,  # NOTE: mocked
                    args,
                )

                if is_registered_command(command):
                    command: Command = get_command(command)
                    result: bool = await command.call(command_payload)
                    return jsonify(success=result)

                # else we consider it as a feedback from reviewer
                elif "/pulls/" in issue_url:
                    review_id = comment_data["pull_request_review_id"]
                    review_url = issue_url + "/reviews/" + str(review_id)
                    review_data = await gh.getitem(review_url)
                    review_status = review_data["state"]
                    if review_status == "APPROVED":
                        reviewer = review_data["user"]["login"]
                        await utils.status(app.gh, issue_url, reviewer)

    return jsonify(success=True)
