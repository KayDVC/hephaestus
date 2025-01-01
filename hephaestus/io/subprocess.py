import logging
import subprocess

from typing import Any, Callable

from hephaestus.common.exceptions import LoggedException
from hephaestus.util.logging import get_logger
from hephaestus.io.stream import LogStreamer

_logger = get_logger(__name__)


# TODO: option to pass the information of the actual caller
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

    Returns:
        The output of the cmd as captured line-by-line. If the command was unsuccessful, None will be returned.

    Notes:
        This function overwrites various commonly set arguments to subprocess.run/subprocess.popen including
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

    # The performance might matter enough here to repeat myself :(.
    cmd_output = []
    retcode = None
    try:
        with subprocess.Popen(cmd, *args, **kwargs) as process:
            if enable_output:
                _logger.log(level=log_level, msg="Cmd Output:")
                for line in process.stdout:
                    line = line.strip()
                    cmd_output.append(line)
                    _logger.log(level=log_level, msg=line)
            else:
                for line in process.stdout:
                    line = line.strip()
                    cmd_output.append(line)

            retcode = process.wait()
    except Exception:
        pass

    return cmd_output if retcode == 0 else None


##
# Public
##
class SubprocessError(LoggedException):
    """Indicates an unexpected error has occurred while attempting a subprocess operation."""

    pass


def command_successful(cmd: list[Any]):
    """Checks if command returned 'Success' status.

    Args:
        cmd: the command to run.

    Note:
        This function doesn't capture or return any command output.
        It's intended to be used in pass/fail-type scenarios involving subprocesses.
    """

    return _exec(cmd, enable_output=False) is not None


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
        cleanup: the function to run in the event of a failure.
        enable_output: whether to log captured output. Defaults to True.
        log_level: the level to log cmd output at. Ignored if enable_output set to False. Defaults to DEBUG.

    Raises:
        SubprocessError if the command fails for any reason.

    Notes:
        This function overwrites various commonly set arguments to subprocess.run/subprocess.popen including
        `stdout`, `stderr`, and `universal_newlines`.

        Users should only expect `enable_output` to change the behavior of what's actually output.
    """
    try:
        if (
            _exec(
                cmd, enable_output=enable_output, log_level=log_level, *args, **kwargs
            )
            is None
        ):
            raise SubprocessError(err)
    except SubprocessError:
        if cleanup:
            cleanup()
        raise
