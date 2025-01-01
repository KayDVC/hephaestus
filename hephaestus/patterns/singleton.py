from threading import Lock

from hephaestus.util.logging import get_logger

_logger = get_logger(__name__)

_singleton_lock = Lock()


class Singleton(type):
    """A Pythonic, thread-safe implementation of the Singleton pattern.

    This class is intended to be used as the meta class for another class.
    i.e.  class MyClass(metaclass=Singleton):
            ...

    Each Singleton object will have access to a standard library thread mutex via `self._lock` for basic thread safety.
    It is the responsibility of the subclass implementer to ensure operations are atomic.

    Final Warnings:
        - If overriding `__call__`, be sure to reference the `__call__` method as implemented in this class.
        - Do not modify `__shared_instances`.
    """

    __shared_instances = {}

    def __call__(cls, *args, **kwargs):
        """Initializes or returns available singleton objects."""

        # Check for object instance before locking.
        if cls not in cls.__shared_instances:

            # Acquire lock and re-check, creating instance as necessary.
            with _singleton_lock:
                if cls not in cls.__shared_instances:

                    _logger.debug(
                        f"Shared instance not available for {cls.__name__}. Creating...",
                        stacklevel=2,
                    )

                    cls.__shared_instances[cls] = super(Singleton, cls).__call__(
                        *args, **kwargs
                    )

                # Add lock for each instance.
                cls._lock = Lock()

        return cls.__shared_instances[cls]  # return instance if available/once created
