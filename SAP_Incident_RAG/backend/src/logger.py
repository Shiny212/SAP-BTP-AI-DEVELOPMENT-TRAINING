"""
logger.py

Centralized logging configuration for the
SAP Incident Knowledge Assistant.

Features
--------
- Console logging
- File logging
- Daily log persistence
- Consistent log formatting
- Reusable singleton logger

Author : Shiny Belsiya
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from src.config import LOG_FILE


class LoggerManager:
    """
    Singleton logger manager.

    Creates one logger instance that can be reused
    throughout the application.
    """

    _logger: logging.Logger | None = None

    @classmethod
    def get_logger(cls) -> logging.Logger:
        """
        Returns the application logger.

        Returns
        -------
        logging.Logger
        """

        if cls._logger is not None:
            return cls._logger

        logger = logging.getLogger("SAPIncidentRAG")

        logger.setLevel(logging.INFO)

        logger.propagate = False

        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        console_handler = logging.StreamHandler()

        console_handler.setLevel(logging.INFO)

        console_handler.setFormatter(formatter)

        Path(LOG_FILE).parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_handler = RotatingFileHandler(
            filename=LOG_FILE,
            maxBytes=5 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8",
        )

        file_handler.setLevel(logging.INFO)

        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

        logger.addHandler(file_handler)

        cls._logger = logger

        return logger


logger = LoggerManager.get_logger()