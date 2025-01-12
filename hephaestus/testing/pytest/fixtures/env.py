import pytest

import hephaestus.patterns.singleton as singleton


@pytest.fixture(scope="function", autouse=True)
def reset_env():
    """Resets Hephaestus memory and such after each test."""
    yield

    # Reset any shared memory
    singleton.clear_all()
