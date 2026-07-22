"""
config/settings.py

Application configuration.
Loads environment variables.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv


# Load .env file
load_dotenv()


GOOGLE_API_KEY = os.getenv(
    "GOOGLE_API_KEY"
)


if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY is missing. Please add it to .env file."
    )