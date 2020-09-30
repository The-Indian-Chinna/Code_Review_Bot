import pytest
from cam2_code_review_bot.static_analysis import PerformanceProfilerTool, StaticAnalyzer


def test_performance_profiler_call_time():
    analyzer: StaticAnalyzer = StaticAnalyzer()
    analyzer.add_tool(PerformanceProfilerTool())
    analyzer.configure_tool_from_file(
        "performance-profiler", "tests/test_performance_profiler/config_01.json"
    )

    output: str = analyzer.run_md()

    fp = open("tests/test_performance_profiler/expected_01.txt", "r")
    expected: str = "".join(fp.readlines())
    fp.close()

    assert output == expected


def test_performance_profiler_number_of_calls():
    analyzer: StaticAnalyzer = StaticAnalyzer()
    analyzer.add_tool(PerformanceProfilerTool())
    analyzer.configure_tool_from_file(
        "performance-profiler", "tests/test_performance_profiler/config_02.json"
    )

    output: str = analyzer.run_md()

    fp = open("tests/test_performance_profiler/expected_02.txt", "r")
    expected: str = "".join(fp.readlines())
    fp.close()

    assert output == expected
