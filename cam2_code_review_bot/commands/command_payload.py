from gidgethub.aiohttp import GitHubAPI
from typing import List, Dict, Any
import json


class CommandPayload:
    """All data passed to a command when `call` is invoked. see `Command` for more information.

    """

    def __init__(
        self,
        gh: GitHubAPI,
        issue_url: str,
        comment_url: str,
        repo_url: str,
        comment_data: Dict[str, Any],
        args: List[str],
    ):
        self.__gh = gh
        self.__issue_url = issue_url
        self.__comment_url = comment_url
        self.__repo_url = repo_url
        self.__comment_data = comment_data
        self.__args = args

    @property
    def gh(self) -> GitHubAPI:
        """GitHubAPI: the github api object for this session. See gidgethub for more information"""
        return self.__gh

    @property
    def issue_url(self) -> str:
        """str: Url for getting an issue"""
        return self.__issue_url

    @property
    def comment_url(self) -> str:
        """str: Url for posting a comment"""
        return self.__comment_url

    @property
    def repo_url(self) -> str:
        """str: Url that points to the given repo"""
        return self.__repo_url

    @property
    def comment_data(self) -> Dict[str, Any]:
        """json: JSON object with all the data about the comment"""
        return self.__comment_data

    @property
    def args(self) -> List[str]:
        """List[str]: All the arguments or "words" after the command"""
        return self.__args
