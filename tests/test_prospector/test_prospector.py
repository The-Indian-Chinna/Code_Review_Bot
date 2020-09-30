import pytest
from cam2_code_review_bot.static_analysis import StaticAnalyzer, ProspectorTool


def test_prospector():
    static_analyzer: StaticAnalyzer = StaticAnalyzer()
    # load the tool(s) we want to test
    static_analyzer.add_tool(ProspectorTool())
    # load the configurations for the tools we want to test
    static_analyzer.configure_tool_from_file("prospector", "tests/test_prospector/config_01.json")
    output: str = static_analyzer.run_md()

    # load the expected results (these should be predefined)
    fp = open("tests/test_prospector/expected_01.txt", "r")
    expected: str = "".join(fp.readlines())
    fp.close()

    assert output == expected
