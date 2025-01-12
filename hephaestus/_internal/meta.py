from pathlib import Path

PROJECT_NAME: str = "Hephaestus"
PROJECT_SOURCE_URL: str = "https://github.com/KayDVC/hephaestus/"

# TODO
PROJECT_DOCUMENTATION_URL: str = ""


class Paths:
    """A collection of paths in the Hephaestus repo.

    Literally, not helpful to anyone but Hephaestus devs.
    """

    ROOT = Path(__file__).parents[2].resolve()
    LOGS = Path(ROOT, "logs")
    LIB = Path(ROOT, "hephaestus")
    CONFIG = Path(ROOT, "config")
    DOCS = Path(ROOT, "docs")

    SPHINX = Path(CONFIG, "sphinx")
