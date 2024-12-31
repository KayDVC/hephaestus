
import logging
import pytest
import _pytest

from hephaestus.util.logging import get_logger


@pytest.fixture(scope="module", autouse=True)
def module_logger(request: _pytest.fixtures.SubRequest):
    """Creates a logger for every test module.

    Args:
        request: the request fixture that gives access to the calling module.

    Yields:
        a logger configured with the name of the test module.
    """
    module_logger = get_logger(file_path=request.path)
    yield module_logger


@pytest.fixture(scope="function", autouse=True)
def logger(request: _pytest.fixtures.SubRequest, module_logger: logging.Logger):
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