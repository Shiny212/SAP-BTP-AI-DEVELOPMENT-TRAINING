"""
config.py

Central configuration module for the SAP Support Agent.

Responsibilities:
- Load environment variables
- Initialize Google Gemini LLM
- Expose reusable application constants
"""

from __future__ import annotations

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# ---------------------------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------------------------

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY not found. Please configure it in the .env file."
    )

# ---------------------------------------------------------------------
# Google Gemini LLM Configuration
# ---------------------------------------------------------------------

MODEL_NAME = "gemini-3.1-flash-lite"

TEMPERATURE = 0.0

llm = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    temperature=TEMPERATURE,
    google_api_key=GOOGLE_API_KEY,
)

# ---------------------------------------------------------------------
# Application Constants
# ---------------------------------------------------------------------

APPLICATION_NAME = "SAP Support Agent"

LOG_FILE = "logs/application.log"

DEFAULT_THREAD_ID = "sap-support-thread"

DEFAULT_CONFIG = {
    "configurable": {
        "thread_id": DEFAULT_THREAD_ID
    }
}