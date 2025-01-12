from collections import namedtuple
from queue import Queue
from typing import Callable

from hephaestus.io.logging import get_logger
from hephaestus.patterns.singleton import Singleton

_logger = get_logger(__name__)

##
# Public
##
MethodTrace = namedtuple("MethodTrace", ["name", "args", "kwargs", "retval"])


class TraceQueue(Queue, metaclass=Singleton):
    """An object capable of storing"""

    def get(self) -> MethodTrace:
        """Returns the last trace.

        Returns:
            The last method trace containing the method's name, the passed
            positional arguments, keyword arguments, and returned value, if any.
        """
        retval = None if self.empty() else super().get()

        return retval

    def clear(self):
        """Removes all MethodTraces from memory."""
        _logger.debug("Clearing trace queue.")
        while not self.empty():
            _ = self.get()


def track(to_track: Callable) -> Callable:
    """Records method call for later examination.

    Args:
        to_track : the method to track.

    Returns:
        The passed method with minor modification pre and post-call
        to support tracking capability.

    Note:
        Can be used as a decorator:

        @track
        def print_copy(*args):
            ...

        Or like a regular method:

        print_copy = track(to_track=print_copy)

    """

    def wrapper(*args, **kwargs):
        """Forward all method parameters to wrapped method."""
        _logger.debug(
            f"Traced method: {to_track.__name__}, Args: {args}, Keyword Args: {kwargs}"
        )

        # Call method and store in queue.
        retval = to_track(*args, **kwargs)
        TraceQueue().put(
            MethodTrace(name=to_track.__name__, args=args, kwargs=kwargs, retval=retval)
        )

        _logger.debug(f"Method returned. Return value: {retval}")
        return retval

    return wrapper
