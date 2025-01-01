from logging import getLogger


class LoggedException(Exception):
    """An exception whose message is logged at the error level.

    This class is meant to be used as the base class for any other custom
    exceptions. It logs the error message for later viewing.
    """

    _logger = getLogger(__name__)

    def __init__(self, msg: str = None):
        self._logger.error(msg)
        super().__init__(msg)
