import logging
import subprocess

from typing import Any, Callable

from hephaestus.common.exceptions import LoggedException, _InternalError
from hephaestus.io.logging import get_logger

_logger = get_logger(__name__)


class _SubprocessError(Exception):
    pass


def _exec(
    cmd: list[Any],
    enable_output: bool = False,
    log_level: int = logging.DEBUG,
    *args,
    **kwargs,
) -> list[str]:
    """Executes a command, logging results as specified.

    Args:
        cmd: the command to run.
        enable_output: whether to log captured output.
        log_level: the level to log cmd output at. Ignored if enable_output set to False. Defaults to DEBUG.

    Raises:
        _Subprocess_Error if the command fails after running.
        Any other exception thrown means there was an issue in the Python runtime logic.

    Returns:
        The output of the cmd as captured line-by-line. If the command was unsuccessful, None will be returned.

    Notes:
        This method overwrites various commonly set arguments to subprocess.run/subprocess.popen including
        `stdout`, `stderr`, and `universal_newlines`.

        Users should only expect `enable_output` to change the behavior of what's actually output.
    """

    # Avoid any non-string shenanigans when printing/executing command.
    cmd = [str(arg) for arg in cmd]
    _logger.debug(f"Running cmd: `{' '.join(cmd)}`")

    # Capture all output.
    kwargs["stdout"] = subprocess.PIPE
    kwargs["stderr"] = subprocess.STDOUT

    # Get the whole line of output before proceeding to the next line.
    kwargs["bufsize"] = 1

    # Make line endings OS-agnostic
    kwargs["universal_newlines"] = True

    try:
        cmd_output = []
        retcode = None
        with subprocess.Popen(cmd, *args, **kwargs) as process:

            # The performance might matter enough here to repeat myself :(.
            if enable_output:
                _logger.log(level=log_level, msg="Cmd Output:")
                for line in process.stdout:
                    line = line.strip()
                    cmd_output.append(line)
                    _logger.log(level=log_level, msg=line)
            else:
                for line in process.stdout:
                    cmd_output.append(line.strip())

            retcode = process.wait()

    # Seriously bad juju here: the code is FUBAR, not the command. Log it.
    except Exception as e:
        raise _InternalError(e)

    if retcode != 0:
        raise _SubprocessError

    return cmd_output


##
# Public
##
class SubprocessError(LoggedException):
    """Indicates an unexpected error has occurred while attempting a subprocess operation."""

    pass


def command_successful(cmd: list[Any], cleanup: Callable = None):
    """Checks if command returned 'Success' status.

    Args:
        cmd: the command to run.
        cleanup: the method to run in the event of a failure. Defaults to None.

    Note:
        This method doesn't capture or return any command output.
        It's intended to be used in pass/fail-type scenarios involving subprocesses.
    """

    success = True

    try:
        _exec(cmd, enable_output=False) is not None

    # Execute cleanup on most exceptions, if available.
    except Exception as e:
        success = False

        if cleanup:
            cleanup()

        # Panic
        if not isinstance(e, _SubprocessError):
            raise

    return success


def run_command(
    cmd: list[Any],
    err: str,
    cleanup: Callable = None,
    enable_output: bool = True,
    log_level: int = logging.DEBUG,
    *args,
    **kwargs,
):
    """Runs command and logs output as specified.

    Args:
        cmd: the command to run.
        err: the error to display if the command fails.
        cleanup: the method to run in the event of a failure. Defaults to None.
        enable_output: whether to log captured output. Defaults to True.
        log_level: the level to log cmd output at. Ignored if enable_output set to False. Defaults to DEBUG.

    Raises:
        SubprocessError if the command fails to return a "success" status.

    Notes:
        This method overwrites various commonly set arguments to subprocess.run/subprocess.popen including
        `stdout`, `stderr`, and `universal_newlines`.

        Users should only expect `enable_output` to change the behavior of what's actually output.
    """
    try:
        _ = _exec(
            cmd, enable_output=enable_output, log_level=log_level, *args, **kwargs
        )

    # Execute cleanup on most exceptions, if available.
    except Exception as e:
        if cleanup:
            cleanup()

        # Command failed after running. Log user provided error message.
        if isinstance(e, _SubprocessError):
            raise SubprocessError(err)

        # Panic
        raise


def get_command_output(
    cmd: list[Any],
    err: str,
    cleanup: Callable = None,
    *args,
    **kwargs,
):
    """Runs command and logs output as specified.

    Args:
        cmd: the command to run.
        err: the error to display if the command fails.
        cleanup: the method to run in the event of a failure. Defaults to None.

    Raises:
        SubprocessError if the command fails to return a "success" status.

    Notes:
        Output via logging is completely disabled here. It's up to the user to
        log the command's output.
    """
    try:
        output = _exec(cmd, enable_output=False, log_level=None, *args, **kwargs)

    # Execute cleanup on most exceptions, if available.
    except Exception as e:
        if cleanup:
            cleanup()

        # Command failed after running. Log user provided error message.
        if isinstance(e, _SubprocessError):
            raise SubprocessError(err)

        # Panic
        raise

    return output
