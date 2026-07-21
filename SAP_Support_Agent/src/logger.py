"""
logger.py

Centralized logging configuration for the SAP Support Agent.

Responsibilities:
- Create log directory automatically
- Configure file and console logging
- Provide a reusable logger instance
"""

from __future__ import annotations

import logging
from pathlib import Path

from src.config import APPLICATION_NAME, LOG_FILE

# ---------------------------------------------------------------------
# Create log directory if it doesn't exist
# ---------------------------------------------------------------------

log_path = Path(LOG_FILE)

log_path.parent.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------
# Configure Logger
# ---------------------------------------------------------------------

logger = logging.getLogger(APPLICATION_NAME)

logger.setLevel(logging.INFO)

# Prevent duplicate handlers when importing multiple times
if not logger.handlers:

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # ----------------------------
    # File Logger
    # ----------------------------
    file_handler = logging.FileHandler(
        filename=LOG_FILE,
        encoding="utf-8",
    )

    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # ----------------------------
    # Console Logger
    # ----------------------------
    console_handler = logging.StreamHandler()

    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # ----------------------------
    # Register Handlers
    # ----------------------------
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# ---------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------

def log_startup() -> None:
    """Log application startup."""
    logger.info("=" * 70)
    logger.info("SAP Support Agent Started")
    logger.info("=" * 70)


def log_shutdown() -> None:
    """Log application shutdown."""
    logger.info("=" * 70)
    logger.info("SAP Support Agent Stopped")
    logger.info("=" * 70)


def log_node(node_name: str) -> None:
    """
    Log execution of a graph node.

    Args:
        node_name: Name of the executing node.
    """
    logger.info("Executing Node: %s", node_name)


def log_tool(tool_name: str) -> None:
    """
    Log execution of a tool.

    Args:
        tool_name: Name of the tool.
    """
    logger.info("Executing Tool: %s", tool_name)


def log_error(error: Exception) -> None:
    """
    Log an exception with traceback.

    Args:
        error: Exception instance.
    """
    logger.exception("Application Error: %s", error)