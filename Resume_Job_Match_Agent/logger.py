"""
logger.py

Application logging configuration.
"""

from __future__ import annotations

import logging
import os

LOG_DIRECTORY = "logs"
LOG_FILE = "application.log"

os.makedirs(LOG_DIRECTORY, exist_ok=True)

LOGGER = logging.getLogger("ResumeJobMatchAgent")

LOGGER.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

file_handler = logging.FileHandler(
    os.path.join(LOG_DIRECTORY, LOG_FILE),
    encoding="utf-8",
)

file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()

console_handler.setFormatter(formatter)

LOGGER.addHandler(file_handler)
LOGGER.addHandler(console_handler)