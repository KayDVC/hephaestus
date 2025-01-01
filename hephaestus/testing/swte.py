from hephaestus.util.logging import get_logger

_logger = get_logger(__name__)
MAX_PRINT_WIDTH = 80
LARGE_DIVIDER = "=" * int(MAX_PRINT_WIDTH / 2)
SMALL_DIVIDER = "-" * MAX_PRINT_WIDTH


class Constants:
    MAGIC_STRING_ONE = "DEADBEEF"
    MAGIC_STRING_TWO = "BADDCAFE"


##
# Logging Functions
##
def large_banner(msg: str, **kwargs):
    """Logs message between dividers.

    :param msg: a string containing the desired text.

    Note:
        Output will look like '...============================ <msg> =============================...'
        Intended to be used with single-line messages only. Multi-line will look strange :).
    """

    # Log message in between dividers.
    _logger.info(f"{LARGE_DIVIDER} {msg} {LARGE_DIVIDER}", **kwargs)


def small_banner(msg: str, **kwargs):
    """Logs message in between some dashes.

    :param msg: a string containing the desired text.

    Note:
        Output will look like:
        '
        ----------------...
        <line 1>
        <line 2>
        ...
        <line n>
        ----------------...
        '
        Safe for use with multi-line messages.
    """

    _logger.info(SMALL_DIVIDER, **kwargs)
    for line in msg.splitlines():
        _logger.info(line, **kwargs)
    _logger.info(SMALL_DIVIDER, **kwargs)
