"""
utils/logger.py

Application logging configuration.
"""

from __future__ import annotations

import logging


logging.basicConfig(
    level=logging.INFO,
    format=
    "%(asctime)s | %(levelname)s | %(message)s",
)


LOGGER = logging.getLogger(
    "Document_QA_RAG"
)