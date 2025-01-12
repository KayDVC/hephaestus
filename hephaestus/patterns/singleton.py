import threading

from typing import Any, Type

from hephaestus.io.logging import get_logger

_logger = get_logger(__name__)


class Singleton(type):
    """A Pythonic, thread-safe implementation of the Singleton pattern.

    This class is intended to be used as the meta class for another class.
    i.e.  class MyClass(metaclass=Singleton):
            ...

    Each Singleton object will have access to a standard library thread mutex via `self._lock` for basic thread safety.
    The type of mutex can be changed by calling the set_lock_type method.

    It is the responsibility of the subclass implementation to ensure ALL operations are atomic.

    Note:
        - Do not directly modify `__shared_instances` nor `__singleton_lock`.
    """

    ##
    # Constants
    ##
    __DEFAULT_LOCK_TYPE: Type = threading.Lock
    __LOCK_ATTR_KEY: str = "_lock"
    __INSTANCE_ATTR_KEY: str = "_instance"

    # Public Access
    DEFAULT_LOCK_TYPE: Type = __DEFAULT_LOCK_TYPE
    LOCK_ATTR_KEY: str = __LOCK_ATTR_KEY
    INSTANCE_ATTR_KEY: str = __INSTANCE_ATTR_KEY

    ##
    # "Private" Class Vars
    ##
    __lock_type: Type = __DEFAULT_LOCK_TYPE
    __shared_instances = {}
    __singleton_lock = __lock_type()

    def __call__(cls, *args, **kwargs):
        """Initializes or returns available singleton objects."""

        # Check for object instance before locking.
        if cls not in cls.__shared_instances:

            # Acquire lock and re-check. Add the attributes necessary for the class to handle
            # its own singleton instantiation.
            with cls.__singleton_lock:
                if cls not in cls.__shared_instances:
                    _logger.debug(
                        f"Known instance of {cls.__name__} not available.",
                    )
                    if not (
                        hasattr(cls, cls.__LOCK_ATTR_KEY)
                        and isinstance(
                            hasattr(cls, cls.__LOCK_ATTR_KEY), cls.__lock_type
                        )
                    ):
                        setattr(cls, cls.__LOCK_ATTR_KEY, cls.__lock_type())
                        _logger.debug(
                            f"Created lock of type {cls.__lock_type.__name__} for {cls.__name__}.",
                        )
                    if not hasattr(cls, cls.__INSTANCE_ATTR_KEY):
                        setattr(cls, cls.__INSTANCE_ATTR_KEY, None)

                    # Prevent race conditions in between releasing this lock and actual instantiation.
                    cls.__shared_instances[cls] = None

        # Follow same double-checked locking pattern here, except, let the class use its
        # own mutex for locking. This should prevent deadlocks where a Singleton requires another
        # Singleton during its instantiation.

        # Also, using the class's fully-qualified name as the key in `__shared_instances` is
        # pretty safe since it should be different for every class. If not, it's probs not written correctly.
        instance = getattr(cls, cls.__INSTANCE_ATTR_KEY)
        lock = getattr(cls, cls.__LOCK_ATTR_KEY)
        if not instance:
            with lock:
                if not instance:
                    instance = super().__call__(*args, **kwargs)  # create object.
                    setattr(cls, cls.__INSTANCE_ATTR_KEY, instance)
                    cls.__shared_instances[cls] = instance
                    _logger.debug(
                        f"Created instance of {cls.__name__}.",
                    )
        else:  # Handle case: class already has instance.
            with lock:
                cls.__shared_instances[cls] = instance

        return getattr(cls, cls.__INSTANCE_ATTR_KEY)


def get_lock_type() -> Type:
    """Returns the current lock type for all Singleton objects.

    Returns:
        The class used to enable atomic operations for all Singleton subclasses
        as well as the Singleton instantiation logic.
    """
    return Singleton._Singleton__lock_type


def set_lock_type(lock_type: Type) -> bool:
    """Sets the lock type for all Singleton objects.

    Args:
        lock_type: a type that, when instantiated, can enable atomic operations for shared data.
            Must support use as a context manager (i.e. `with lock_type():`).

    Returns:
        True if the pass lock_type was set; False otherwise.

    Note:
        This should be called before any Singleton instantiation due to ensure safe operations.
    """

    # Ensure we were given a class.
    if not isinstance(lock_type, Type):
        _logger.warning(
            f"Lock Type {str(lock_type)} is not a class. Keeping current lock type: {get_lock_type().__name__}"
        )

    # Test with context management. This is what the singleton logic uses and probs what extenders will use.
    try:
        with lock_type():
            pass
    except Exception:
        _logger.warning(
            f"Custom lock type cannot be used with context management. Keeping current lock type: {get_lock_type().__name__}. "
        )
        return False

    # Change lock type.
    current_singleton_lock = (
        Singleton._Singleton__singleton_lock
    )  # Assignment to a local var here is not actually necessary, just helps me sleep better at night.
    with current_singleton_lock:
        Singleton._Singleton__lock_type = lock_type
        Singleton._Singleton__singleton_lock = lock_type()

    return True


def clear_all():
    """Destroys all known Singleton instances."""
    _logger.debug("Clearing all known Singleton instances.")
    with Singleton._Singleton__singleton_lock:

        shared_instances = Singleton._Singleton__shared_instances

        for cls in shared_instances.keys():
            if getattr(cls, Singleton.INSTANCE_ATTR_KEY):
                with getattr(cls, Singleton.LOCK_ATTR_KEY):
                    setattr(cls, Singleton.INSTANCE_ATTR_KEY, None)
                    shared_instances[cls] = None
