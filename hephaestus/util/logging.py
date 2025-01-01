import logging
import inspect
import sys
import time

from pathlib import Path
from typing import Callable, Optional

from hephaestus.common.types import PathLike
from hephaestus.common.colors import Colors

"""
    A wrapper for the logging interface that ensures a consistent logging experience.
    
    Many classes utility functions in this file are defined elsewhere for public use, however,
    their use would cause a circular dependency.
"""

# Allow users to override default color for log levels.
_original_record_factory = logging.getLogRecordFactory()


def record_factory(*args, **kwargs):
    record = _original_record_factory(*args, **kwargs)
    if color_override := kwargs.get("color", None):
        record.color = color_override
    return record


logging.setLogRecordFactory(record_factory)


class FormatOptions:
    """Format Options for a logging.Formatter.

    Args:
        fmt: the format string to use
        default_color: the ANSI color code used to color output.
        style: the 'format' style to use. '{', '%'
    """

    def __init__(self, fmt: str, default_color: str, style: str):
        self.fmt = fmt
        self.default_color = default_color
        self.style = style


##
# Formatting
##
class LogFormatter(logging.Formatter):
    """Defines common message format for files.

    Args:
        enable_color: whether formatter should include ASCII-based coloring.
        time_expr: the method to convert seconds since epoch to a time.struct_time object.
        fmt_opts: a mapping of the format options to use for each level.
    """

    _SHORT_FMT = "[{asctime}] {levelname:7}: {message}"
    _VERBOSE_FMT = f"{_SHORT_FMT} ({{name}}:{{funcName}}:{{lineno}})"
    _FMT_STYLE = "{"

    DEFAULT_ENABLE_COLOR = True
    DEFAULT_TIME_EXPR = time.gmtime
    DEFAULT_FORMAT_OPTS = {
        logging.DEBUG: FormatOptions(
            fmt=_VERBOSE_FMT, default_color=Colors.MAGENTA, style=_FMT_STYLE
        ),
        logging.INFO: FormatOptions(
            fmt=_SHORT_FMT, default_color=Colors.CYAN, style=_FMT_STYLE
        ),
        logging.WARNING: FormatOptions(
            fmt=_VERBOSE_FMT, default_color=Colors.YELLOW, style=_FMT_STYLE
        ),
        logging.ERROR: FormatOptions(
            fmt=_VERBOSE_FMT, default_color=Colors.RED, style=_FMT_STYLE
        ),
        logging.CRITICAL: FormatOptions(
            fmt=_VERBOSE_FMT, default_color=Colors.RED, style=_FMT_STYLE
        ),
    }

    def __init__(
        self,
        enable_color: Optional[bool] = True,
        time_expr: Optional[Callable] = None,
        fmt_opts: Optional[dict[int, FormatOptions]] = None,
    ):
        super().__init__()
        self._enable_color = enable_color
        self._time_expr = time_expr if time_expr else self.DEFAULT_TIME_EXPR
        self._formatters = self._construct_formatters(fmt_opts)

    def _create_formatter(self, fmt: str, style: str) -> logging.Formatter:
        """Creates log formatters from string and time expression method.

        Args:
            fmt: the template for the formatter as defined in logging docs.
            style: the 'format' style to use. '{', '%'.

        Returns:
            A ready-to-go formatting object.
        """
        formatter = logging.Formatter(fmt=fmt, style=style)
        formatter.converter = self._time_expr

        return formatter

    def _construct_formatters(
        self, fmt_opts: dict[int, FormatOptions]
    ) -> dict[int, logging.Formatter]:
        """Creates formatter objects.

        Args:
            fmt_opts: a mapping of the format options to use for each level.

        Returns:
            A formatter object for each log level with the specified template.
        """
        if not fmt_opts:
            fmt_opts = self.DEFAULT_FORMAT_OPTS

        formatters = {}
        for level, opts in fmt_opts.items():
            fmt = opts.fmt
            formatters[level] = self._create_formatter(fmt, opts.style)

        return formatters

    def format(self, record):
        """Converts log record into customized format.

        Args:
            record: logging object (attributes + message).

        Returns:
            A formatted string.
        """
        formatted_str = self._formatters[record.levelno].format(record)

        if not self._enable_color:
            return formatted_str

        return f"{getattr(record, "color", self.DEFAULT_FORMAT_OPTS[record.levelno].default_color)}{formatted_str}{Colors.RESET}"


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
    enable_color: Optional[bool] = LogFormatter.DEFAULT_ENABLE_COLOR,
    time_expr: Optional[Callable] = LogFormatter.DEFAULT_TIME_EXPR,
    fmt_opts: Optional[dict[int, FormatOptions]] = LogFormatter.DEFAULT_FORMAT_OPTS,
):
    """Configures logger that ever other logger propagates up to.

    Args:
        min_level: the minimum log level to pipe to stdout. Defaults to logging.INFO.
        log_file: the absolute path to the log file to generate. Defaults to None.
        enable_color: whether output to stdout should be colored. Defaults to LogFormatter.DEFAULT_ENABLE_COLOR.
        time_expr: a method that converts the seconds since the epoch to a time.struct_time
            object. Defaults to LogFormatter.DEFAULT_TIME_EXPR.
        fmt_opts: a mapping of the format options to use for each level. Defaults to LogFormatter.DEFAULT_FMT_OPTS.

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
            LogFormatter(
                enable_color=(
                    False
                    if (isinstance(handler, logging.FileHandler) or (not enable_color))
                    else True
                ),
                time_expr=time_expr,
                fmt_opts=fmt_opts,
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
