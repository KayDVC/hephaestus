import logging
import inspect
import sys
import time

from pathlib import Path
from typing import Callable

from hephaestus.common.types import PathLike
from hephaestus.common.colors import Colors

"""
    A wrapper for the logging interface that ensures a consistent logging experience.
    
    Many classes utility functions in this file are defined elsewhere for public use, however,
    their use would cause a circular dependency.
"""

##
# Formatting
##
class _LogFormatter(logging.Formatter):
    """Defines common message format for files."""

    _FMT = "[{asctime}] {levelname:7}: {message} ({name}:{funcName}:{lineno})"

    _COLORED_FORMATS = {
        logging.DEBUG: Colors.GREEN + _FMT + Colors.RESET,
        logging.INFO: Colors.CYAN + _FMT + Colors.RESET,
        logging.WARNING: Colors.YELLOW + _FMT + Colors.RESET,
        logging.ERROR: Colors.RED + _FMT + Colors.RESET,
    }

    _PLAIN_FORMATS = {
        logging.DEBUG: _FMT,
        logging.INFO: _FMT,
        logging.WARNING: _FMT,
        logging.ERROR: _FMT,
    }

    def __init__(self, color: bool, time_expr: Callable):
        """
        Args:
            color: whether formatter should include ASCII-based coloring.
            time_expr: the method to convert seconds since epoch to a time.struct_time object.
        """
        super().__init__()
        self._time_expr = time_expr
        self._formatters = self._construct_formatters(self._COLORED_FORMATS if color else self._PLAIN_FORMATS)

    def _create_formatter(self, fmt: str) -> logging.Formatter:
        """Creates log formatters from string and time expression method.

        Args:
            fmt: the template for the formatter as defined in logging docs.
            time_expr: the method to convert seconds since epoch to a time.struct_time object.

        Returns:
            A ready-to-go formatting object.
        """

        formatter = logging.Formatter(fmt=fmt, style="{")

        # Express log time in UTC rather than local time
        formatter.converter = self._time_expr

        return formatter

    def _construct_formatters(
        self, fmt_dict: dict[int, str]
    ) -> dict[int, logging.Formatter]:
        """Creates formatter objects.

        Args:
            fmt_dict: a mapping of format template to each log level.

        Returns:
            A formatter object for each log level with the specified template.
        """
        formatters = {}
        for level, fmt in fmt_dict.items():
            formatters[level] = self._create_formatter(fmt)

        return formatters

    def format(self, record):
        """Converts log record into customized format.

        Args:
            record: logging object (attributes + message).

        Returns:
            A formatted string.
        """
        return self._formatters[record.levelno].format(record)


##
# Log Configuration
##

__last_sh = None
__last_fh = None


def _create_log_folder(log_file: Path) -> bool:
    """Attempts to create the parent of the log file.

    Args:
        log_file: the file where logs will be stored to.

    Returns:
        True if the the parent directory of log_file exists. False otherwise.

    Note:
        There is no guarantee that an existing directory will enable the program to write
        a file to the directory at this time.
    """
    if not log_file:
        return False

    if not log_file.parent.exists():
        log_file.parent.mkdir(parents=True)

    # TODO: return true only if directory exists and program is able to write to it.
    return log_file.parent.exists()


def configure_root_logger(
    min_level: int = logging.INFO,
    log_file: PathLike = None,
    color: bool = True,
    time_expr: Callable = time.gmtime,
):
    """Configures logger that ever other logger propagates up to.

    Args:
        min_level: the minimum log level to pipe to stdout. Defaults to logging.INFO.
        log_file: the absolute path to the log file to generate. Defaults to None.
        color: whether output to stdout should be colored. Defaults to True.
        time_expr: a method that converts the seconds since the epoch to a time.struct_time
            object. Defaults to time.gmtime

    Note:
        If log_file is provided, a file will attempt to be generated. Logs saved to file will never
        contain colored output.
    """
    global __last_sh
    global __last_fh

    # Convert to
    if log_file:
        log_file = Path(log_file).resolve()

    # Configure settings for logger.
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Prep to configure handlers.
    handlers = []
    log_folder_available = _create_log_folder(log_file)

    # Pipe to standard out at specified level.
    if __last_sh is None:
        __last_sh = logging.StreamHandler(sys.stdout)
        handlers.append(__last_sh)
    __last_sh.setLevel(min_level)  # allow level updating on the fly.

    # Remove any existing file handlers.
    if log_folder_available and (__last_fh is not None):
        logger.removeHandler(__last_fh)
        __last_fh.close()

    # (and) Pipe to file if specified; include all messages. Log file creation will be
    # skipped if the log folder does not exist at this point for any reason.
    if log_file and log_folder_available:
        __last_fh = logging.FileHandler(log_file, mode="w")
        __last_fh.setLevel(logging.DEBUG)
        handlers.append(__last_fh)

    # Apply common configurations and add to logger object.
    for handler in handlers:
        handler.setFormatter(
            _LogFormatter(
                color=(
                    False
                    if (isinstance(handler, logging.FileHandler) or (not color))
                    else True
                ),
                time_expr=time_expr,
            )
        )
        logger.addHandler(handler)


def get_logger(
    name: str = None, root: PathLike = None, file_path: PathLike = None
) -> logging.Logger:
    """Creates a log of application activity.

    Args:
        name: the name of the calling module. Defaults to None.
        root: the path to the root of the project. Defaults to none.
        file_path: the path to the file where this logger will be used. Only use this
        parameter when fine control over logger naming is necessary.

    Returns:
        A bare logger object that accepts all default levels of log messages.

    Note:
        If the calling file is not in the project and the `name` arg is provided,
        this acts just like logging.getLogger(name). If the file is in the project AND
        the `root` arg is provided, the name will be relative to the root of the project.
        If `file_path` is specified, it will be used to name the logger instead of the calling
        file.
    """
    # Convert supplied path to absolute path.
    if root:
        root = Path(root).resolve()

    # Get logger
    if root and root.exists():
        try:
            file_path = (
                Path(file_path).resolve()
                if file_path
                else Path(inspect.stack()[1].filename).resolve()
            )
            name = ".".join(file_path.relative_to(root).with_suffix("").parts)
        except ValueError:
            pass

    # Generate logger object that accepts all messages. Filtering will be done at the root level.
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    return logger
