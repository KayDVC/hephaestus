import pytest

from hephaestus.patterns.singleton import Singleton


@pytest.fixture(scope="function", autouse=True)
def reset_env():
    """Resets Hephaestus memory and such after each test."""
    yield

    # Reset any shared memory
    Singleton._Singleton__shared_instances.clear()
