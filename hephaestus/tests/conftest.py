import logging
import sys

from hephaestus.io.stream import LogStreamer
from hephaestus.testing.fixtures import *
from hephaestus.util.logging import get_logger

__logger = get_logger()

sys.stdout = LogStreamer(logger=__logger, log_level=logging.INFO)
# sys.stderr = LogStreamer(logger=__logger, log_level=logging.WARNING)
