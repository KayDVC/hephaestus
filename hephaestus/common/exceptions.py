import textwrap

from logging import getLogger
from typing import Any

from hephaestus._internal.meta import PROJECT_SOURCE_URL


class LoggedException(Exception):
    """An exception whose message is logged at the error level.

    This class is meant to be used as the base class for any other custom
    exceptions. It logs the error message for later viewing.
    There is only one argument added to the basic Exception `__init__` method; see args below.
    
    Args:
        stack_level: the number of calls to peek back in the stack trace for
            log info such as function name, line number, etc.
    """

    _logger = getLogger(__name__)

    def __init__(self, msg: Any = None, stack_level: int = 2, *args):
        """_summary_

        Args:
            msg: _description_. Defaults to None.
            stack_level: _description_. Defaults to 2.
        """
        self._logger.error(msg, stacklevel=stack_level)
        super().__init__(msg, *args)

class _InternalError(LoggedException):
    """Indicates a problem with the library's code was encountered.
    """
    
    def __init__(self, msg: Any = None, *args):
        msg = textwrap.dedent(
        f"""\
        Encountered an internal error with the Hephaestus Library:
        \t{msg}
        \tPlease report this issue here: {PROJECT_SOURCE_URL}
        """
        )
        super().__init__(msg, stack_level=3, *args)
