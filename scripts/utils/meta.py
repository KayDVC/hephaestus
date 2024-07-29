from pathlib import Path

"""
    A collection of meta data concerning Hephaestus for use across all Python-based scripts.
    
    Currently includes:
        - Common file locations (absolute)
"""
class Meta:
    ROOT = Path(Path(__file__).parent, "..", "..").resolve()    
    PINCLUDE = Path(ROOT, "include", "hephaestus")
    SRC = Path(ROOT, "src")
    