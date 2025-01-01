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
def logger(module_logger: logging.Logger):
    """Provides the module's logger.

    Args:
        module_logger: the logger generated for the module.

    Yields:
        A ready-to-use logger object.
    """
    yield module_logger
