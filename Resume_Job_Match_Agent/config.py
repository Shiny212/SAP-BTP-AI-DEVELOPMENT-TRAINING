"""
config.py

Loads environment variables and initializes the Gemini LLM.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
MODEL_NAME: str = os.getenv("MODEL_NAME", "gemini-3.1-flash-lite")
TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0"))

llm = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    google_api_key=GOOGLE_API_KEY,
    temperature=TEMPERATURE,
)