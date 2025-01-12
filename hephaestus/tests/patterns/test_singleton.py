import threading

from queue import Queue
from typing import Callable

from hephaestus.io.logging import get_logger
from hephaestus.patterns.singleton import set_lock_type, get_lock_type, Singleton
from hephaestus.testing.swte import StrConsts
from hephaestus.testing.mock.threading import MockLock

# Annotations
import logging

_logger = get_logger(__name__)


class FakeClassOne(metaclass=Singleton):
    pass


class FakeClassTwo(metaclass=Singleton):
    pass


class TestSingleton:

    def _execute_possible_deadlock_test(
        self, test_case: Callable, expect_deadlock: bool = False
    ):

        fail_buffer_secs = 2

        # We'll want to use an abortable mutex to ensure test suite it affected.
        _logger.debug("Changing singleton to use MockLock class.")
        assert set_lock_type(lock_type=MockLock)

        # Share data between threads using atomic operations.
        shared_queue = Queue()
        shared_queue.put(_logger)
        shared_queue.put(MockLock)

        def handle_deadlock(shared_queue: Queue):

            logger = shared_queue.get()
            logger.warning("Deadlock detected. Attempting to recover.")

            # Empty queue and abort test case
            MockLock = shared_queue.get()
            MockLock.abort()

        _logger.debug(f"Setting a {fail_buffer_secs}s test case timeout.")
        fail_timer = threading.Timer(
            interval=2, function=handle_deadlock, kwargs={"shared_queue": shared_queue}
        )
        fail_timer.start()

        _logger.debug(f"Running test case.")
        test_case()

        fail_timer.cancel()

        # Revert any changes made during test
        assert set_lock_type(lock_type=Singleton.DEFAULT_LOCK_TYPE) and (
            get_lock_type() is Singleton.DEFAULT_LOCK_TYPE
        )
        assert shared_queue.empty() == expect_deadlock

    def test_deadlock_helper(self):
        """Verifies utility method properly detects and fails a test case when it triggers a deadlock."""

        def guaranteed_deadlock():
            lock = MockLock()
            with lock:
                with lock:
                    pass

        self._execute_possible_deadlock_test(
            test_case=guaranteed_deadlock, expect_deadlock=True
        )

    def test_same_instance(self, logger: logging.Logger):
        """Verifies multiple instantiation attempts on a single class only result in one object."""

        logger.info("Creating objects")
        obj1 = FakeClassOne()
        obj2 = FakeClassOne()

        logger.info("Comparing objects")
        assert obj1 is obj2

    def test_has_mutex(self, logger: logging.Logger):
        """Verifies each object is created with a mutex."""

        logger.info("Creating objects")
        obj1 = FakeClassOne()

        logger.info("Checking for mutex")
        assert hasattr(obj1, Singleton.LOCK_ATTR_KEY)

    def test_different_mutex_objects(self, logger: logging.Logger):
        """Verifies each object has a personal mutex."""

        logger.info("Creating objects")
        obj1 = FakeClassOne()
        obj2 = FakeClassTwo()

        logger.info(
            "Checking uniqueness of mutexes"
        )  # mutexes? muticies? mutecie? may it's weird and always spelled with the singular version like moose.
        assert getattr(obj1, Singleton.LOCK_ATTR_KEY) is not getattr(
            obj2, Singleton.LOCK_ATTR_KEY
        )

    def test_persistent_data(self, logger: logging.Logger):
        """Verifies each instantiation of an object has the same data available."""

        class FakeClassWithData(metaclass=Singleton):
            def __init__(self):
                self.data = []

        logger.info("Creating objects")
        obj1 = FakeClassWithData()

        obj1.data.append(StrConsts.DEADBEEF)

        obj2 = FakeClassWithData()

        logger.info("Checking for persistent data across both objects")
        assert obj1.data == obj2.data

    def test_nested_instantiation(self, logger):
        """Verifies Singleton objects do not cause deadlocks when instantiated
        inside other Singleton objects"""

        class ParentSingleton(metaclass=Singleton):
            def __init__(self):
                self.nested_singleton = FakeClassOne()

        def test_case():
            _ = ParentSingleton()

        self._execute_possible_deadlock_test(test_case=test_case, expect_deadlock=False)
