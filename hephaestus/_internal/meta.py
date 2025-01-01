from pathlib import Path


class Paths:
    ROOT = Path(__file__).parents[2].resolve()
    LOGS = Path(ROOT, "logs")
    LIB = Path(ROOT, "hephaestus")
    CONFIG = Path(ROOT, "config")
    DOCS = Path(ROOT, "docs")

    SPHINX = Path(CONFIG, "sphinx")
