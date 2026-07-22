"""
config/settings.py

Application configuration.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv


load_dotenv()


GOOGLE_API_KEY = os.getenv(
    "GOOGLE_API_KEY"
)


if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY is missing in .env file"
    )