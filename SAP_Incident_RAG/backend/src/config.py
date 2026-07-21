"""
config.py

Centralized application configuration for the
SAP Incident Knowledge Assistant.

All project constants, paths, environment variables,
model names, and retrieval settings are defined here.

Author: Shiny Belsiya
Project: SAP Incident Knowledge Assistant using Structured Data RAG
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# ---------------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------------

load_dotenv()

# ---------------------------------------------------------
# Project Paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"

LOG_DIR = PROJECT_ROOT / "logs"

CHROMA_DB_PATH = PROJECT_ROOT / "chroma_db"

SCREENSHOT_DIR = PROJECT_ROOT / "screenshots"

DOCUMENTS_DIR = PROJECT_ROOT / "docs"

# Create directories automatically

for directory in (
    DATA_DIR,
    LOG_DIR,
    CHROMA_DB_PATH,
    SCREENSHOT_DIR,
    DOCUMENTS_DIR,
):
    directory.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------
# Files
# ---------------------------------------------------------

EXCEL_FILE = DATA_DIR / "sap_incidents.xlsx"

LOG_FILE = LOG_DIR / "application.log"

# ---------------------------------------------------------
# Google Gemini Configuration
# ---------------------------------------------------------

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise EnvironmentError(
        "GOOGLE_API_KEY not found. "
        "Please configure it inside the .env file."
    )

CHAT_MODEL = "gemini-3.1-flash-lite"

EMBEDDING_MODEL = "gemini-embedding-001"

# ---------------------------------------------------------
# Dataset Configuration
# ---------------------------------------------------------

DATASET_NAME = "SAP Incident Dataset"

SOURCE_TYPE = "Structured Excel"

SHEET_NAME = "Sheet1"

# ---------------------------------------------------------
# Chunking Configuration
# ---------------------------------------------------------

CHUNK_SIZE = 1200

CHUNK_OVERLAP = 150

# ---------------------------------------------------------
# Retrieval Configuration
# ---------------------------------------------------------

DEFAULT_TOP_K = 5

MAX_TOP_K = 10

SIMILARITY_THRESHOLD = 0.70

# ---------------------------------------------------------
# Vector Store Configuration
# ---------------------------------------------------------

COLLECTION_NAME = "sap_incidents"

DISTANCE_METRIC = "cosine"
# ---------------------------------------------------------
# Embedding / Vector Store Configuration
# ---------------------------------------------------------

EMBEDDING_BATCH_SIZE = 10

MAX_RETRIES = 10

RETRY_WAIT_SECONDS = 25


# ---------------------------------------------------------
# Metadata Fields
# ---------------------------------------------------------

METADATA_FIELDS = [
    "source_type",
    "source_name",
    "sheet_name",
    "row_number",
    "incident_id",
    "sap_module",
    "priority",
    "category",
    "owner_team",
]

# ---------------------------------------------------------
# Supported Analytical Keywords
# ---------------------------------------------------------

ANALYTICAL_KEYWORDS = [
    "average",
    "count",
    "maximum",
    "minimum",
    "sum",
    "highest",
    "lowest",
    "how many",
    "statistics",
]

# ---------------------------------------------------------
# Console
# ---------------------------------------------------------

LINE = "=" * 90