import pytest
from cam2_code_review_bot.static_analysis import StaticAnalyzer, VultureTool


def test_vulture():
    """Runs vulture on a file with dead code
    """

    static_analyzer: StaticAnalyzer = StaticAnalyzer()
    # load the tool(s) we want to test
    static_analyzer.add_tool(VultureTool())
    # load the configurations for the tools we want to test
    static_analyzer.configure_tool_from_file("vulture", "tests/test_vulture/vulture_config_01.json")
    output: str = static_analyzer.run_md()

    # load the expected results (these should be predefined)
    fp = open("tests/test_vulture/expected_vulture_01.txt", "r")
    expected: str = "".join(fp.readlines())
    fp.close()

    assert type(output) is str and output == expected


def test_vulture_invalid_file_type():
    """Checks that VultureTool throws an error when a non python file is provided as input
    """

    static_analyzer: StaticAnalyzer = StaticAnalyzer()
    # load the tool(s) we want to test
    static_analyzer.add_tool(VultureTool())
    # load the configurations for the tools we want to test
    with pytest.raises(
        ValueError, match=r'Invalid file type provided\. File must have the extension "\.py"'
    ):
        static_analyzer.configure_tool_from_file(
            "vulture", "tests/test_vulture/vulture_config_02.json"
        )


def test_vulture_invalid_config_file():
    """Checks that VultureTool throws an error when the config file does not contain the correct fields
    """

    static_analyzer: StaticAnalyzer = StaticAnalyzer()
    # load the tool(s) we want to test
    static_analyzer.add_tool(VultureTool())
    # load the configurations for the tools we want to test
    with pytest.raises(ValueError, match=r"Invalid config file\. \[\w+\] not defined\."):
        static_analyzer.configure_tool_from_file(
            "vulture", "tests/test_vulture/vulture_config_03.json"
        )
