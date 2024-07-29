import logging
import inspect
from pathlib import Path
from .meta import Meta

"""
    A wrapper for the logging interface that ensures a consistent logging experience.
    
    Currently includes:
        - Common file locations (absolute)
"""

class Formatter(logging.Formatter):
    """Defines common message format for files."""

    # no explicit constructor necessary.
    class Colors:
        CYAN    = "\033[36m"
        GREEN   = "\033[32m"
        RED     = "\033[31m"
        YELLOW  = "\033[33m"
        RESET   = "\033[0m"

    minimal_details = "%(levelname)-7s: %(message)s "
    full_details = "%(levelname)-7s [%(asctime)s]: %(message)s (%(name)s:%(lineno)s)"
    LEVEL_STYLES = {
        logging.DEBUG: Colors.GREEN + minimal_details + Colors.RESET,
        logging.INFO: Colors.CYAN + minimal_details + Colors.RESET,
        logging.WARNING: Colors.YELLOW + minimal_details + Colors.RESET,
        logging.ERROR: Colors.RED + full_details + Colors.RESET,
    }

    def format(self, record):
        """Converts log record into customized format.

        Args:
            record: logging object (attributes + message).

        Returns:
            A formatted string.
        """
        log_format = self.LEVEL_STYLES[record.levelno]
        return logging.Formatter(log_format).format(record)


def get_logger(verbose:bool=False) -> logging.Logger:
    """Creates a log of application activity.

    Args:
        verbose (bool): whether to include all logging levels or only warnings and higher.
        Defaults to false.

    Returns:
        A logger object that outputs information to standard output.
    """
    
    # ensure logs get propagated upstream
    name = f"{Path(inspect.stack()[1].filename).relative_to(Meta.ROOT)}"
    
    # generate logger object.
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # accept all messages globally.

    log_formatter = Formatter()

    # add handler for stdout.
    std_out_handler = logging.StreamHandler()
    std_out_handler.setLevel(logging.DEBUG if verbose else logging.WARNING)  # display messages based on specified verbosity.
    std_out_handler.setFormatter(log_formatter)
    logger.addHandler(std_out_handler)

    return logger