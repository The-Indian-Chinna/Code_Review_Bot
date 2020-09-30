import pytest
from typing import List
from cam2_code_review_bot.static_analysis import StaticTool, StaticError, StaticAnalyzer

"""
Mocked errors for testing purposes
"""

error_01: StaticError = StaticError(
    file_path="test.py",
    line_no=5,
    code="if is_basic_error(__file__):",
    error_id=0,
    error_name="Basic Error",
    error_description="this is a basic error for testing purposes",
    tool_name="basic-error-tool",
    is_false_positive=False,
    pull_request=0,
    commit_hash="",
)

error_02: StaticError = StaticError(
    file_path="test.py",
    line_no=12,
    code="print (not_printable_object)",
    error_id=0,
    error_name="Basic Error",
    error_description="this is a basic error for testing purposes",
    tool_name="basic-error-tool",
    is_false_positive=False,
    pull_request=0,
    commit_hash="",
)

error_03: StaticError = StaticError(
    file_path="test.py",
    line_no=21,
    code="3 + an_object",
    error_id=1,
    error_name="Different Basic Error",
    error_description="this is a different basic error for testing purposes",
    tool_name="basic-error-tool",
    is_false_positive=False,
    pull_request=0,
    commit_hash="",
)


class BasicErrorGenTool(StaticTool):
    """Mocks a basic tool for testing purposes
    """

    def __init__(self, errors: List[StaticError]):
        self.errors = errors
        super(BasicErrorGenTool, self).__init__("basic-error-tool")

    def load_config(self, config) -> None:
        pass

    def run(self) -> List[StaticError]:
        return self.errors


def _test_markdown_helper(errors: List[StaticError], expected_file: str):
    """Abstracts mardown test  
    """
    sa: StaticAnalyzer = StaticAnalyzer()
    sa.add_tool(BasicErrorGenTool(errors))
    output: str = sa.run_md()

    fp = open(expected_file, "r")
    expected: str = "".join(fp.readlines())
    fp.close()

    assert output == expected


def test_markdown():
    """Tests that markdown is generated properly
    """
    _test_markdown_helper([error_01, error_02], "tests/test_markdown/expected_markdown_01.txt")


def test_markdown_no_errors():
    """Tests that the correct response is returned from the StaticAnalyzer when no errors are found
    """
    _test_markdown_helper([], "tests/test_markdown/expected_markdown_02.txt")


def test_markdown_single_error():
    """Tests that markdown is generated properly for a single error
    """
    _test_markdown_helper([error_01], "tests/test_markdown/expected_markdown_03.txt")


def test_markdown_different_errors():
    """Tests that markdown is generated properly for different errors
    """
    _test_markdown_helper(
        [error_01, error_02, error_03], "tests/test_markdown/expected_markdown_04.txt"
    )
