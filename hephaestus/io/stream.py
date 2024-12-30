import logging
import inspect

class LogStreamer:
    """A streaming interface that enables write operations directly to logger object.
    """
    
    def __init__(self, logger: logging.Logger, log_level: int = logging.INFO):
        """
        Args:
            logger: the logger object to stream output to.
            log_level: the logging level to stream output at. Defaults to logging.INFO.
        """
        self._logger = logger
        self._log_level = log_level
        
    def write(self, msg, *args):
        """Logs passed information at specified level.
        """
        # msg = str(msg).strip()
        if len(msg) > 0:
            self._logger.log(level=self._log_level, msg = msg, *args)
        
    def flush(self):
        """Flushes the handlers for each stream available to the logger.
        """
        # for handler in self._logger.handlers:
        #     handler.flush()
        pass
    
    def isatty(self) -> bool:
        """Returns whether the logger has an output stream available.

        Returns:
            True if the logger has at least one handler; False otherwise.
        """
        return len(self._logger.handlers) > 0