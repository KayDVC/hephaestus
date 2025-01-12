import logging
import os
import pytest
import _pytest

from pathlib import Path

import hephaestus.testing.swte as swte
from hephaestus.common.constants import CharConsts
from hephaestus.io.logging import get_logger


@pytest.fixture(scope="module", autouse=True)
def module_logger(request: _pytest.fixtures.SubRequest):
    """Creates a logger for every test module.

    Args:
        request: the request fixture that gives access to the calling module.

    Yields:
        a logger configured with the name of the test module.
    """
    module_path = Path(request.path).relative_to(Path(request.session.startpath))
    logger_name = str(module_path.with_suffix("")).replace(os.sep, ".")

    module_logger = get_logger(name=logger_name)
    swte.large_banner(
        request.module.__name__.upper().replace(CharConsts.UNDERSCORE, CharConsts.SPACE)
    )
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
