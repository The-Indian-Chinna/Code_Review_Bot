import pytest
from cam2_code_review_bot.static_analysis import StaticAnalyzer, DuplicateTool


def test_duplicate1():
    """
    Runs duplicate tool on a file with cloned lines of code
    """

    static_analyzer = StaticAnalyzer()
    # load the tool(s) we want to test
    static_analyzer.add_tool(DuplicateTool())
    # load the configurations for the tools we want to test
    static_analyzer.configure_tool_from_file("duplicate", "tests/test_duplicate/test1_config.json")
    output = static_analyzer.run_md()
    # load the expected results (these should be predefined)

    fp = open("tests/test_duplicate/expected_duplicate_1.txt", "r")
    expected: str = "".join(fp.readlines())
    fp.close()

    assert type(output) is str and output == expected


def test_duplicate2():
    """
    Runs duplicate tool on a more complex file with cloned lines of code
    """

    static_analyzer = StaticAnalyzer()
    # load the tool(s) we want to test
    static_analyzer.add_tool(DuplicateTool())
    # load the configurations for the tools we want to test
    static_analyzer.configure_tool_from_file("duplicate", "tests/test_duplicate/test2_config.json")
    output = static_analyzer.run_md()
    # load the expected results (these should be predefined)

    fp = open("tests/test_duplicate/expected_duplicate_2.txt", "r")
    expected: str = "".join(fp.readlines())
    fp.close()

    assert type(output) is str and output == expected


def test_minval():
    """
    Testing min value configuration
    """

    static_analyzer = StaticAnalyzer()
    # load the tool(s) we want to test
    static_analyzer.add_tool(DuplicateTool())
    # load the configurations for the tools we want to test
    static_analyzer.configure_tool_from_file("duplicate", "tests/test_duplicate/test3_config.json")
    output = static_analyzer.run_md()
    # load the expected results (these should be predefined)

    fp = open("tests/test_duplicate/expected_duplicate_3.txt", "r")
    expected: str = "".join(fp.readlines())
    fp.close()


def test_many_errors():
    """
    Test one error per line configuration
    """
    static_analyzer = StaticAnalyzer()
    # load the tool(s) we want to test
    static_analyzer.add_tool(DuplicateTool())
    # load the configurations for the tools we want to test
    static_analyzer.configure_tool_from_file("duplicate", "tests/test_duplicate/test4_config.json")
    output = static_analyzer.run_md()
    # load the expected results (these should be predefined)
    fp = open("tests/test_duplicate/expected_duplicate_4.txt", "r")
    expected: str = "".join(fp.readlines())
    fp.close()


def test_ignore():
    """
    Test ignore syntatic constructs configuration
    """
    static_analyzer = StaticAnalyzer()
    # load the tool(s) we want to test
    static_analyzer.add_tool(DuplicateTool())
    # load the configurations for the tools we want to test
    static_analyzer.configure_tool_from_file("duplicate", "tests/test_duplicate/test5_config.json")
    output = static_analyzer.run_md()
    # load the expected results (these should be predefined)
    fp = open("tests/test_duplicate/expected_duplicate_5.txt", "r")
    expected: str = "".join(fp.readlines())
    fp.close()
