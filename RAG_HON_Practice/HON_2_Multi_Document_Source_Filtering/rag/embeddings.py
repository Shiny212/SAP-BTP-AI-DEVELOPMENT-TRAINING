"""
rag/embeddings.py

Google Generative AI embeddings.
"""

from __future__ import annotations

from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
)

from config.settings import GOOGLE_API_KEY


def get_embedding_model():
    """
    Create Google embedding model.
    """

    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=GOOGLE_API_KEY,
    )


def create_embeddings(
    texts: list[str],
) -> list[list[float]]:
    """
    Generate embeddings for multiple chunks.
    """

    model = get_embedding_model()

    return model.embed_documents(
        texts
    )


def create_query_embedding(
    text: str,
) -> list[float]:
    """
    Generate embedding for user question.
    """

    model = get_embedding_model()

    return model.embed_query(
        text
    )