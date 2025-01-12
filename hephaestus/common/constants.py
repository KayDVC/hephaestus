class AnsiColors:
    """ANSI escape codes representing various colors."""

    CYAN = "\033[36m"
    GREEN = "\033[32m"
    RED = "\033[31m"
    YELLOW = "\033[33m"
    MAGENTA = "\033[35m"
    RESET = "\033[0m"


class CharConsts:
    """Common characters."""

    NULL = ""
    SPACE = " "
    UNDERSCORE = "_"


class StrConsts:
    """Common strings."""

    EMPTY_STRING = CharConsts.NULL


class Emojis:
    """Common graphical symbols that represent various states or ideas."""

    GREEN_CHECK = "✅"
    RED_CROSS = "❌"
    GOLD_MEDAL = "🏅"
