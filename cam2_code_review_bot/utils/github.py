import json
import asyncio
import aiohttp
from typing import List, Any, Dict
from gidgethub.aiohttp import GitHubAPI


class Github:
    """API for interacting with github 

    The goal of this class is to abstract github developer endpoints into functions

    Note:
        This class is not complete. 
    """

    _github_api: GitHubAPI = None

    @staticmethod
    def initialize(github_api: GitHubAPI) -> None:
        """Sets the `GitHubAPI` object to use when fulfilling requests

        Args:
            github_api (GitHubAPI): The github object this module should use.
        """
        Github._github_api = github_api

    @staticmethod
    def _get_valid_api_object() -> GitHubAPI:
        """Gets the GitHubAPI object

        Raises:
            RuntimeError: The GitHubAPI object is not defined.

        Returns:
            GitHubAPI: The current GitHubAPI object.
        """

        if Github._github_api is None:
            raise RuntimeError("No GitHubAPI object is defined. Please call initialize first.")
        else:
            return Github._github_api

    @staticmethod
    async def get_pull_request_files_metadata(pull_request_url: str) -> Dict[str, Any]:
        """Gets pull request file metadata from github

        See [github developer docs](https://developer.github.com/v3/pulls/#list-pull-requests-files) 
        for more information.

        Args:
            pull_request_url (str): The url endpoint for a pull request. This should have the format 
                "/repos/{owner}/{repo}/pulls/{pull_number}" where:
                - {owner} is the repo owner
                - {repo} is the name of the repo
                - {pull_number} is the number of the pull request

        Raises:
            RuntimeError: The GitHubAPI object is not defined. (see init)

        Returns:
            json: The response object from the GitHub Developer AP (see github developer docs).

        """
        github_api: GitHubAPI = _get_valid_api_object()
        return await github_api.getitem(pull_request_url + "/files")

    @staticmethod
    async def get_pull_request_files_rawdata(pull_request_url: str) -> tuple:
        """Gets pull request file raw data from github

        Raw data is the content of the files. However because a http response is returned, alongside
        the raw data, the files encoding and if it was successfully downloaded are returned as well. 

        Args:
            pull_request_url (str): The url endpoint for a pull request. This should have the format 
                "/repos/{owner}/{repo}/pulls/{pull_number}" where:
                - {owner} is the repo owner
                - {repo} is the name of the repo
                - {pull_number} is the number of the pull request

        Raises:
            RuntimeError: The GitHubAPI object is not defined. (see init)

        Returns:
            tuple: A tuple of the http responses from downloading each file

        """
        github_api: GitHubAPI = _get_valid_api_object()
        file_metadata: Dict[str, Any] = get_pull_request_files_metadata(
            pull_request_url, github_api
        )

        file_data_list: tuple = await asyncio.gather(
            [github_api.getitem(file["contents_url"]) for file in file_metadata]
        )
        response: tuple = await asyncio.gather(
            [aiohttp.get(file_data["download_url"]) for file_data in file_data_list]
        )

        return response

    @staticmethod
    async def save_pull_request_files_to_dir(pull_request_url: str, directory: str) -> List[str]:
        """Saves pull request files from github to a relative local directory

        See [github developer docs](https://developer.github.com/v3/pulls/#list-pull-requests-files) 
        for more information.

        Args:
            pull_request_url (str): The url endpoint for a pull request. This should have the format 
                "/repos/{owner}/{repo}/pulls/{pull_number}" where:
                - {owner} is the repo owner
                - {repo} is the name of the repo
                - {pull_number} is the number of the pull request

            directory (str): The directory to save the files. This should be relative to the 
                root directory of this project.

        Raises:
            RuntimeError: The GitHubAPI object is not defined. (see init)

        Returns:
            List[str]: A list of the file names that were saved

        """
        # Set to valid directory
        if not directory.endswith("/"):
            directory = directory + "/"

        github_api: GitHubAPI = _get_valid_api_object()
        file_metadata: Dict[str, Any] = get_pull_request_files_metadata(
            pull_request_url, github_api
        )

        file_data_list: tuple = await asyncio.gather(
            [github_api.getitem(file["contents_url"]) for file in file_metadata]
        )
        response: tuple = await asyncio.gather(
            [aiohttp.get(file_data["download_url"]) for file_data in file_data_list]
        )

        file_list: List[str] = [file_data["name"] for file_data in file_data_list]

        with open(directory + file_name, "w+", encoding=response.encoding) as local_file:
            local_file.write(response.text)

        return file_list
