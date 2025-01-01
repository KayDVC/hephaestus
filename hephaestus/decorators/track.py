from collections import namedtuple
from queue import Queue
from typing import Callable

from hephaestus.util.logging import get_logger
from hephaestus.patterns.singleton import Singleton

_logger = get_logger(__name__)

##
# Public
##
FunctionTrace = namedtuple("FunctionTrace", ["name", "args", "kwargs", "retval"])


class Trace_Queue(Queue, metaclass=Singleton):
    """An object capable of storing"""

    def get() -> FunctionTrace:
        """_summary_

        Returns:
            _description_
        """

        retval = None

        if retval:
            retval = super().get()

        return retval


def track(to_track: Callable) -> Callable:
    """Records function call for later examination.

    Args:
        to_track : the function to track.

    Returns:
        The passed function with minor modification pre and post-call
        to support tracking capability.

    Note:
        Can be used as a decorator:

        @track
        def print_copy(*args):
            ...

        Or like a regular function:

        print_copy = track(to_track=print_copy)

    """

    def wrapper(*args, **kwargs):
        """Forward all function parameters to wrapped function."""
        _logger.debug(
            f"Traced method: {to_track.__name__}, Args: {args}, Keyword Args: {kwargs}"
        )

        # Call function and store in queue.
        retval = to_track(*args, **kwargs)
        Trace_Queue().put(
            FunctionTrace(
                name=to_track.__name__, args=args, kwargs=kwargs, retval=retval
            )
        )

        _logger.debug(f"Method returned. Return value: {retval}")
        return retval

    return wrapper
