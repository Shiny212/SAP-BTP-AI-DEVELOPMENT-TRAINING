"""
embeddings.py

Gemini Embedding Service

Responsibilities
----------------
1. Initialize Gemini Embedding Model
2. Validate API configuration
3. Return reusable embedding instance

Author : Shiny Belsiya
"""

from __future__ import annotations

from langchain_google_genai import GoogleGenerativeAIEmbeddings

from src.config import EMBEDDING_MODEL, GOOGLE_API_KEY
from src.logger import logger


class EmbeddingService:
    """
    Singleton Embedding Service.
    """

    _embedding_model = None

    @classmethod
    def get_embeddings(cls) -> GoogleGenerativeAIEmbeddings:
        """
        Return Gemini Embedding Model.

        Returns
        -------
        GoogleGenerativeAIEmbeddings
        """

        if cls._embedding_model is not None:
            return cls._embedding_model

        logger.info("Initializing Gemini Embedding Model...")

        cls._embedding_model = GoogleGenerativeAIEmbeddings(
            model=EMBEDDING_MODEL,
            google_api_key=GOOGLE_API_KEY,
            task_type="retrieval_document",
        )

        logger.info("Gemini Embedding Model Initialized Successfully.")

        return cls._embedding_model