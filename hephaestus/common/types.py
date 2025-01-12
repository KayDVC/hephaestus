import os

from typing import Any, Union
from pathlib import Path


PathLike = Union[str, Path, os.PathLike]


def to_bool(obj: Any):
    """Converts any object to a boolean.

    Args:
        obj: the object to convert.

    Returns:
        True if the object has a sane truthy value; False otherwise.
    """
    if not isinstance(obj, str):
        return bool(obj)

    obj = obj.lower()

    return obj in ["true", "t", "yes", "y", "enable"]
