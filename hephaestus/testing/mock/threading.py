from typing import Any

import logging
from hephaestus.common.exceptions import LoggedException


class MockMutexAbort(LoggedException):
    def __init__(self, msg: Any):
        super().__init__(msg=msg, log_level=logging.WARNING, stack_level=3)


class MockLock:
    """A simple implementation of a Mutex without any frills.

    This class is capable of aborting an operation by calling MockLock.abort().
    """

    _abort_operation = False

    def __init__(self):
        self._locked = False

    def acquire(self):
        """Waits until lock is available, then acquires the lock."""
        while self._locked:

            # Entirety of abort lock. Nice and simple.
            if self._abort_operation:
                self._abort_operation = False
                raise MockMutexAbort("Aborting operation requiring lock.")

            continue

        self._locked = True

    def release(self):
        """Releases a lock. Can be called even without lock being acquired."""
        self._locked = False

    @classmethod
    def abort(cls):
        """Releases deadlocked mutex."""
        cls._abort_operation = True

    ##
    # Enable use as a context manager
    ##
    def __enter__(self):
        return self.acquire()

    def __exit__(self, exception_type, *args, **kwargs) -> bool:
        self.release()
        return exception_type is MockMutexAbort
