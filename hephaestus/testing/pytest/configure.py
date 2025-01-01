import logging
import pytest
import sys
import time

import hephaestus.testing.swte as swte

from collections import namedtuple
from typing import Any

from hephaestus.io.stream import LogStreamer, NullStreamer
from hephaestus.util.logging import get_logger, LogFormatter

# PyTest Devs think everything should be private for some reason.
import _pytest
import _pytest.config
import _pytest.nodes
import _pytest.reports
import _pytest.runner
import _pytest.terminal

"""
This module contains various configurations and custom hook implementations for PyTest.

It's best to import all of the content like so:
    ```
    # File: conftest.py
    from hephaestus.testing.pytest.configure import *
    ```
Most methods build off of others 

All method and method argument names need to be exactly as stated in the PyTest API spec. Because of this, and many other 
things, there's no need to document each param. Annotations are still incredibly helpful.
"""

##
# Types
##
OutcomeMap = namedtuple("OutcomeMap", ["log_level", "to_string"])
TestResult = namedtuple("TestResult", ["outcome", "failure_trace"])

##
# Constants
##
# TODO: Reason from `pytest.mark.<skip, xfail>` not propagating. Might be best to implement a custom wrapper that stores the reason in swte.py.
OUTCOME_MAPS: {str, OutcomeMap} = {
    # Success with no strings attached.
    "PASSED": OutcomeMap(log_level=logging.INFO, to_string=lambda report: "PASSED"),
    # Indicate a test was skipped or marked as known failure. We want these to be somewhat prominent in the logs.
    "SKIPPED": OutcomeMap(
        log_level=logging.WARNING,
        to_string=lambda report: f"Marked to be skipped. Reason: {getattr(report, 'wasxfailed', 'Not provided')}",
    ),
    "XFAILED": OutcomeMap(
        log_level=logging.WARNING,
        to_string=lambda report: f"Marked as known failure. Reason: {getattr(report, 'wasxfailed', 'Not provided')}",
    ),
    # Trouble. A test failed outright or we expected it to fail and it passed; either way, something isn't right.
    "FAILED": OutcomeMap(
        log_level=logging.ERROR, to_string=lambda report: f"FAILED {report.nodeid}"
    ),
    "XPASSED": OutcomeMap(
        log_level=logging.WARNING,
        to_string=lambda report: f"Marked as failure, but passed. Believed to fail because: {getattr(report, 'wasxfailed', 'Not provided')}",
    ),
}
SUCCESS = 0
FAIL = 1


# Log all output from automated tests.
root_logger = get_logger(name="root")
sys.stdout = LogStreamer(logger=root_logger)
sys.stderr = LogStreamer(logger=root_logger, log_level=logging.ERROR)

# Store each test result for final summary.
test_results: dict[str, dict[str, TestResult]] = {
    key: {} for key in OUTCOME_MAPS.keys()
}

# Keep running tally of execution time excluding overhead.
test_execution_time: float = 0.00


##
# Utility
##
def _get_failure_repr(report: _pytest.reports.TestReport) -> str:
    """Extracts test's failure reason if available.

    :param report: the Test report for a given phase of testing.
    :return: the string representation of the cause of test failure if available. If not, an empty string.
    """
    return "\n".join(
        report.longreprtext.splitlines()[1:]
    )  # The first line is an address to the function which is not useful


@pytest.hookimpl(trylast=True)  # Going last ensures out removal is not overridden.
def pytest_configure(config: _pytest.config.Config) -> None:
    """Disable the terminal entirely.

    Note:
        In order to customize the output to terminal even a little, you'd have to
        rewrite about 250+ lines of incredibly obtuse internal PyTest code.

        If not doing this, you either have to deal with uncolored results (which are somewhat
        difficult to parse at a glance) or ANSI codes showing up in the log file (also difficult to parse).

        Instead we'll just use various public hooks to log the results of each test.
    """
    if config.pluginmanager.has_plugin("terminalreporter"):
        reporter = config.pluginmanager.get_plugin("terminalreporter")
        reporter._tw._file = NullStreamer()


@pytest.hookimpl(wrapper=True, trylast=True)
def pytest_runtest_makereport(item: _pytest.nodes.Item, call: _pytest.runner.CallInfo[None]) -> _pytest.reports.TestReport:  # type: ignore
    """Logs each function's docstring.

    Note:
        This is done here instead of in the fixture because the function level fixtures don't run when a function is marked to be skipped.
        We always want to know what would be run and why it wasn't.
    """
    test_report = yield

    # Print function's docstring and name.
    if test_report.when == "setup":
        swte.small_banner(
            f"Name: {item.function.__name__}\nDescription: {item.function.__doc__}"
        )

    return test_report


@pytest.hookimpl
def pytest_exception_interact(
    call: _pytest.runner.CallInfo[Any], report: _pytest.reports.TestReport
) -> None:
    """Logs failure/exception message as it's thrown."""

    # Log unexpected failure when it happens. We'll display it again in the summary.
    if call.excinfo:
        code_rep = _get_failure_repr(report=report)
        root_logger.error(code_rep)


@pytest.hookimpl(wrapper=True, trylast=True)
def pytest_report_teststatus(report: _pytest.reports.CollectReport | _pytest.reports.TestReport, config: _pytest.config.Config) -> _pytest.terminal.TestShortLogReport:  # type: ignore
    """Logs and saves the result of the test."""
    global test_execution_time
    global test_results

    # This log_report can have any of the 5 outcomes in OUTCOME_MAPS. All functions only have "passed", "failed", or "skipped".
    log_report = _pytest.terminal.TestShortLogReport(*(yield))
    outcome = log_report.category.upper()

    # Log the outcome of the test even if it doesn't run.
    if (report.skipped and report.when == "setup") or (report.when == "call"):

        # Obtuse PyTest logic may also force this hook to run unexpectedly. We only want to log the test result in this way once.
        if not test_results[outcome].get(report.nodeid, None):

            test_execution_time += report.duration
            outcome_map = OUTCOME_MAPS[outcome]
            root_logger.log(
                level=outcome_map.log_level, msg=outcome_map.to_string(report)
            )

            test_results[outcome][report.nodeid] = TestResult(
                outcome=outcome, failure_trace=_get_failure_repr(report=report)
            )

    return log_report


@pytest.hookimpl
def pytest_unconfigure(config: _pytest.config.Config):
    """Display test stats and summary before exiting."""

    reporter = config.pluginmanager.get_plugin("terminalreporter")

    swte.large_banner("Completed Execution ")

    # Give each result category a more descriptive name.
    description_map = {
        "Tests Passed": "PASSED",
        "Tests Skipped": "SKIPPED",
        "Expected Failures": "XFAILED",
        "Unexpected Passes": "XPASSED",
        "Unexpected Failures": "FAILED",
    }

    # Gather Stats
    test_stats = {
        desc: len(test_results[category]) for desc, category in description_map.items()
    }
    test_stats["Total Tests"] = sum(list(test_stats.values()))
    test_stats["Test Execution Time (s)"] = f"{test_execution_time: 3f}"
    test_stats["Total Execution Time (s)"] = (
        f"{(time.time() - reporter._sessionstarttime): 3f}"
    )

    # Log Stats
    for desc, value in test_stats.items():
        root_logger.info(f"{desc}: {value}")

    # Log Test Results Again
    for desc, category in description_map.items():

        # Skip result categories that weren't encountered during run.
        results_for_category = test_results[category]
        if len(results_for_category) == 0:
            continue

        # Since the "interactive" part is over, everything we display will be at the "info" level.
        # To make it easier to differentiate between result category severity levels, we'll override the color
        # depending on the result category.
        log_level = OUTCOME_MAPS[category].log_level
        category_color = LogFormatter.DEFAULT_FORMAT_OPTS[log_level].default_color
        swte.large_banner(msg=desc, extra={"color": category_color})

        for test_name, results in results_for_category.items():
            # Redisplay stack trace for each failed test.)
            if category == "FAILED":
                msg = f"{test_name} : {results.outcome}\n{results.failure_trace}"
                swte.small_banner(msg=msg, extra={"color": category_color})

            else:
                root_logger.info(
                    f"{test_name} : {results.outcome}", extra={"color": category_color}
                )


@pytest.hookimpl
def pytest_sessionfinish(
    session: _pytest.main.Session, exitstatus: int | _pytest.config.ExitCode
):
    """Returns the status of the program based on test failures."""

    # If there was a failure triggered for any reason other than the tests, respect it.
    if exitstatus == SUCCESS:
        exitstatus = (
            FAIL
            if ((len(test_results["FAILED"]) + len(test_results["XPASSED"])) > 0)
            else SUCCESS
        )

    exit(exitstatus)
