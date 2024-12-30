import logging
import pytest

from hephaestus.patterns.singleton import Singleton
from hephaestus.util.logging import get_logger

"""
Note:
    We use pytest.FixtureRequest as the type of request in this module,
    but it's really SubRequest. Our uses will only interact with the information
    made available from the parent FixtureRequest class so, it's good enough
    for annotation and type hinting purposes.
"""


@pytest.fixture(scope="module", autouse=True)
def module_logger(request: pytest.FixtureRequest):
    """Creates a logger for every test module.

    Args:
        request: the request fixture that gives access to the calling module.

    Yields:
        a logger configured with the name of the test module.
    """
    module_logger = get_logger(file_path=request.path)
    yield module_logger


@pytest.fixture(scope="function", autouse=True)
def logger(request: pytest.FixtureRequest, module_logger: logging.Logger):
    """Logs each function's docstring and provides the module's logger.

    Args:
        request: the request fixture that gives access to the calling function.
        module_logger: the logger generated for the module.

    Yields:
        A ready-to-use logger object.
    """
    module_logger.info(f"Name: {request.function.__name__}")
    module_logger.info(f"Description: {request.function.__doc__}")

    yield module_logger


@pytest.fixture(scope="function", autouse=True)
def cleanup():
    """Resets Hephaestus memory and such after each test."""
    yield
    
    # make a small space after test name for readability.
    print("\n")

    # Reset any shared memory
    Singleton._Singleton__shared_instances.clear()
