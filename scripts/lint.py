import argparse
import pathlib
import subprocess

from utils.meta import Meta

# Utility Meta Data
VERSION = "1.0.0"

OK = lambda: exit(0)
FAIL = lambda: exit(1)

"""
    A utility to check or fix the format of all Python and C++ files.

    Utilizes Black and Clang Format.
"""


def get_cpp_files() -> list[str]:
    """Gets the file names of all C++ files in the include and src directory
    recursively.

    Returns:
        A list of all file *.h and *.cpp files.
    """
    files = (
        # Public includes
        list(pathlib.Path(Meta.PINCLUDE).rglob("*.h"))
        +
        # Source files
        list(pathlib.Path(Meta.SRC).rglob("*.h"))
        + list(pathlib.Path(Meta.SRC).rglob("*.cpp"))
    )
    return files


def check_format(fix: bool) -> bool:
    """_summary_

    Args:
        fix (bool): whether formatting errors should be corrected inplace.

    Returns:
        True if all files properly formatted; false otherwise.

    Note:
        Success message only displays information related to Python files.
    """

    # Clang Format does not have a recursive option, therefore, the simplest solution
    # is to pass all of the files via CLI.
    cpp_files = get_cpp_files()

    if len(cpp_files) > 0:

        # Generate command backwards due to non-similar arguments
        cmd = cpp_files

        # Fix error inplace. Will write directly to files.
        if fix:
            cmd.append("-i")

        # Do a dry run. If one formatting error is found, the command fails.
        else:
            cmd.extend(
                [
                    "1",  # Set error limit to 1
                    "--ferror-limit",
                    "--Werror",  # Turn format problems into errors.
                    "--dry-run",
                ]
            )

        cmd.append("clang-format")
        cmd.reverse()

        if subprocess.run(cmd).returncode:
            FAIL()

    # Black handles recursive file search because it's just better :).
    cmd = [
        "black",
        Meta.SCRIPTS,
    ]
    if not fix:
        cmd.append("--check")

    if subprocess.run(cmd).returncode:
        FAIL()


def main():

    parser = argparse.ArgumentParser(
        prog="Lint",
        description="Lints/Formats all C++ files using Clang-Format and Python files using Black",
        usage="python lint.py --fix",
    )

    parser.add_argument(
        "-f",
        "--fix",
        default=False,
        dest="fix",
        required=False,
        action="store_true",
        help="Fix formatting issues in place. Writes to files",
    )

    parser.add_argument(
        "-v",
        "--version",
        default=False,
        dest="version",
        required=False,
        action="store_true",
        help="Print version of the script.",
    )
    args = parser.parse_args()

    if args.version:
        print(f"v{VERSION}")
        return

    check_format(args.fix)
    OK()


if __name__ == "__main__":
    main()
