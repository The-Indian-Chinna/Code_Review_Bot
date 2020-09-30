import pytest
from cam2_code_review_bot.static_analysis import StaticAnalyzer, PyflakesTool


def test_pyflakes():
    """Runs pyflakes on a file with dead code
    """

    static_analyzer: StaticAnalyzer = StaticAnalyzer()
    # load the tool(s) we want to test
    static_analyzer.add_tool(PyflakesTool())
    # load the configurations for the tools we want to test
    static_analyzer.configure_tool_from_file("pyflakes", "tests/test_pyflakes/config_01.json")
    output: str = static_analyzer.run_md()

    # load the expected results (these should be predefined)
    fp = open("tests/test_pyflakes/expected_01.txt", "r")
    expected: str = "".join(fp.readlines())
    fp.close()

    assert type(output) is str and output == expected
