import yaml
import argparse
from pathlib import Path
from utils.logger import get_logger
from utils.meta import Meta

"""
    A simple utility to generate CMake files for each submodule in the Hephaestus Library.
    
    The script can be called from the current working directory (CWD) or given a path relative 
    to the CWD containing the source of the submodule using the `--submodule-path`.
    
    By default, the script will look for a file named `config.yml` in the submodule directory,
    however, all values specified in the configuration file can be overridden using the command 
    line arguments.
"""
# Utility Meta Data
VERSION = "v1.0.0"

# Set to a logger object before use.
logger = None

submodule_config = {
    "name": None,
    "dependencies": [],
    "files_to_exclude": [],
}


##
# Utilities
##
def get_source_files(path: Path) -> str:
    """Creates a string of all source files in submodule directory.

    Args:
        path (Path): the path to the source directory.

    Returns:
        A string containing all of the source files in the submodule directory excluding
        the files specified.
    """

    # Get all C or C++ source and header files, excluding files as necessary. Note,
    # the script assumes there can be internal/private header files declared within the source
    # module. Any header meant to be publicly accessible should be defined in the "include" folder.
    source_files = []
    for file in [
        f
        for f in path.iterdir()
        if (
            f.is_file()
            and (f.suffix in [".cpp", ".c", ".hpp", ".h"])
            and (f.stem not in submodule_config["files_to_exclude"])
        )
    ]:
        source_files.append(file.name)
    
    normalized_files = "\n".join(source_files)
    logger.debug(f"Source files retrieved:\n{normalized_files}")
    
    return "\n".join(source_files)


def get_header_files(path: Path) -> str:
    """Creates a string of all header files in matching public include directory.

    Args:
        path (Path): the path to the source directory.

    Returns:
        A string containing all of the header files under a matching public header directory excluding
        the files specified.

    Note:
        The relative path from `src` to the submodule is used to find the the public header directory.
        I.e The following condition must be met:
            `src`/<...>/submodule_src = `include/hephaestus`/<...>/submodule_headers
    """
    
    path = Path(Meta.PINCLUDE, path.relative_to(Meta.SRC)) 
    
    # Get all C or C++ header files, excluding files as necessary.
    header_files = []
    for file in [
        f
        for f in path.iterdir()
        if (
            f.is_file()
            and (f.suffix in [".hpp", ".h"])
            and (f.stem not in submodule_config["files_to_exclude"])
        )
    ]:
        header_files.append(f"${{PROJECT_SOURCE_DIR}}/{file.relative_to(Meta.ROOT)}")
    
    normalized_files = "\n".join(header_files)
    logger.debug(f"Header files retrieved:\n{normalized_files}")

    return normalized_files

def draft_template(path: Path) -> str:

    template = (
f"""
## 
# Generated using `Generate Submodule Cmake Lists Utility` {VERSION}
##

# Create a variable to use in place of submodule name
set(subm_name {submodule_config["name"]})

# Add all source and header files in submodule
add_library(${{subm_name}}
{get_source_files(path)}
{get_header_files(path)}
)

# Ensure submodule accessible using hephaestus::<submodule_name>.
# Note, does not account for nested folders.
add_library(${{PROJECT_NAME}}::${{subm_name}} ALIAS ${{subm_name}})

# Submodule Meta Data
set_target_properties(${{subm_name}} PROPERTIES VERSION ${{PROJECT_VERSION}})
set_target_properties(${{subm_name}} PROPERTIES SOVERSION ${{PROJECT_VERSION_MAJOR}})
"""
)

    if len(submodule_config["dependencies"]) > 0:
        template += (
f"""
# Include internal/external dependencies.
target_link_libraries(${{subm_name}} PUBLIC
{"\n".join(submodule_config["dependencies"])}
)
"""
        )
    
    
    logger.debug(f"Generated Template:\n{template}")
    logger.info("Template successfully generated.")
        
    return template

##
# File I/O
##
def read_config_file(path: Path):
    """Reads and sets submodule parameters based on configuration file.

    Args:
        path (Path): the path to the submodule.
    """
    logger.info("Attempting to read Yaml Configuration File.")
    config_file = Path(path, "config.yml")

    # Nothing to read
    if not config_file.is_file():
        logger.warning(f"Failed to find configuration file in: {path}")
        return

    # Attempt to read YAML configuration file.
    with config_file.open() as f:
        try:
            config_data = yaml.safe_load(f)
        except:
            logger.error(f"Failed to open configuration file: \n\t{config_file}")
            raise

    # Set submodule configuration when available
    if name := config_data.get("Submodule Name"):
        logger.info(f"Received submodule name: {name}")
        submodule_config["name"] = name

    # Dependencies can be internal or external in the config file.
    # If internal, we want to leave the string interpolation to CMake.
    if internal_deps := config_data.get("Internal Dependencies"):
        for dep in internal_deps:
            logger.info(f"Received internal dependency: {dep}")
            submodule_config["dependencies"].append(f"${{PROJECT_NAME}}::{dep}")
    if external_deps := config_data.get("External Dependencies"):
        for dep in external_deps:
            logger.info(f"Received external dependency: {dep}")
            submodule_config["dependencies"].append(f"{dep}")

    if files_to_exclude := config_data.get("Exclude Files"):
        for file in files_to_exclude:
            logger.info(f"Received file to exclude: {file}")
            submodule_config["files_to_exclude"].append(f"{file}")

def write_cmake_file(path:Path, template:str):
    """Saves passed CMake template to `CMakeLists.txt` in directory specified.

    Args:
        path (Path): the path to the submodule.
        template (str): the generated CMake script template to write.
    """
    cmake_file = Path(path, "CMakeLists.txt")
    
    try:
        with cmake_file.open('w') as f:
            f.write(template)
    except:
        logger.error(f"Failed to create CMake file at:\n{cmake_file}")
        raise
    
    logger.info(f"Wrote template to CMake file at:\n{cmake_file}")

def main():
    global logger

    parser = argparse.ArgumentParser(
        prog="Generate Submodule CMake Script",
        description="Creates 'CMakeLists.txt' in a the current folder",
    )
    parser.add_argument(
        "-p",
        "--submodule-path",
        default="",
        dest="path",
        required=False,
        help="The path to the submodule relative to the current directory.",
    )
    parser.add_argument(
        "-n",
        "--submodule-name",
        default=None,
        dest="name",
        required=False,
        help="The submodule name.",
    )
    parser.add_argument(
        "-d",
        "--submodule-dependencies",
        default=None,
        dest="dependencies",
        nargs="+",
        required=False,
        help="A list of dependencies for the submodule.",
    )
    parser.add_argument(
        "-e",
        "--exclude-submodule-files",
        default=None,
        dest="files_to_exclude",
        nargs="+",
        required=False,
        help="A list of source files in the submodule to exclude.",
    )
    parser.add_argument(
        "-vv",
        "--verbose",
        default=False,
        dest="verbose",
        required=False,
        action="store_true",
        help="Print all script logs",
    )
    parser.add_argument(
        "-v",
        "--version",
        default=False,
        dest="version",
        required=False,
        action="store_true",
        help="Print version of the script",
    )
    args = parser.parse_args()
    
    if args.version:
        print(VERSION)
        return

    logger = get_logger(args.verbose)

    # Determine whether expected path is valid
    path = Path(Path.cwd(), args.path)
    if path.is_file():
        logger.error(f"Expected path to a directory.")
        return
    
    if not path.is_dir():
        logger.error(f"Unable to find path: \n\t{path}")
        return

    # Extract configuration if available.
    read_config_file(path)

    # Replace extracted configuration with passed arguments as necessary.
    if args.name:
        logger.info(
            f"Received submodule name: {args.name}. {
                'Overriding name from configuration file.' if submodule_config.get('name') else ''
                }"
        )
        submodule_config["name"] = args.name
    if not (submodule_config.get("name")):
        submodule_config["name"] = path.stem
        logger.info(
            f"Inferred submodule name from directory: {submodule_config["name"]}"
        )
    if args.dependencies:
        logger.info(
            f"Received dependencies: {args.dependencies}.\n {
                'Overriding dependencies from configuration file.' if (len(submodule_config['dependencies']) > 0) else ''}"
        )
        submodule_config["dependencies"] = args.dependencies

    if args.files_to_exclude:
        logger.info(
            f"Received files to exclude: {args.files_to_exclude}.\n {
                'Overriding files to exclude from configuration file.' if (len(submodule_config['files_to_exclude']) > 0) else ''}"
        )
        submodule_config["files_to_exclude"] = args.files_to_exclude
    
    # Create CMakeLists.txt file for the given module.
    write_cmake_file(path, draft_template(path))
    
if __name__ == "__main__":
    main()
