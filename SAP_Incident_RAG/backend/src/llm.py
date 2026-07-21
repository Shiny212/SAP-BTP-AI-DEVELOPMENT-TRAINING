"""
llm.py

Enterprise Gemini LLM Service

Responsibilities
----------------
1. Initialize Gemini Chat Model
2. Generate Responses
3. Centralized LLM Configuration

Author : Shiny Belsiya
"""

from __future__ import annotations

from langchain_google_genai import ChatGoogleGenerativeAI

from src.config import (
    CHAT_MODEL,
    GOOGLE_API_KEY,
)
from src.logger import logger


class LLMService:
    """
    Gemini LLM Service.
    """

    @staticmethod
    def get_llm() -> ChatGoogleGenerativeAI:
        """
        Return configured Gemini Chat model.
        """

        logger.info(
            "Initializing Gemini Chat Model..."
        )

        llm = ChatGoogleGenerativeAI(
            model=CHAT_MODEL,
            google_api_key=GOOGLE_API_KEY,
            temperature=0.2,
            max_tokens=1024,
        )

        logger.info(
            "Gemini Chat Model Initialized Successfully."
        )

        return llm