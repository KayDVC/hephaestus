import os
from pathlib import Path

from hephaestus.common.exceptions import LoggedException
from hephaestus.common.types import PathLike
from hephaestus.util.logging import get_logger

_logger = get_logger(__name__)

##
# Public
##

# Defined in hephaestus.common.types
"""
PathLike: A string, Path, or similar representation of a file path.
"""


class FileError(LoggedException):
    """Indicates an error has occurred while attempting a file operation."""

    pass


def validate_path(path: PathLike) -> Path:
    """Resolves a path and verifies it exists.

    Args:
        path: the path to validate.

    Returns:
        A path object resolved to be absolute.

    Raises:
        FileError: if the path cannot be found.
    """

    # Convert to Path object with absolute path.
    path = Path(path).resolve()
    _logger.debug(f"Attempting to find path: {path}")

    # Ensure path actually exists.
    if not path.exists():
        raise FileError(f"Path {str(path)} does not exists.")

    return path


def create_directory(path: PathLike) -> Path:
    """Attempts to create directory at specified location.

    Args:
        folder: the path to the directory.

    Returns:
        A Path object with the path to the directory.

    Raises:
        FileError if directory creation failed.

    """
    # Convert to Path object with absolute path.
    path = Path(path).resolve()
    _logger.debug(f"Attempting to create directory: {path}")

    path.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        raise FileError(f"Failed to create directory : {str(path)}.")

    return path
