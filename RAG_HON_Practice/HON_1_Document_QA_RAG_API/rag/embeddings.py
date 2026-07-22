"""
rag/embeddings.py

Google Generative AI embedding generation.
"""

from __future__ import annotations

from langchain_google_genai import GoogleGenerativeAIEmbeddings

from config.settings import GOOGLE_API_KEY


def get_embedding_model() -> GoogleGenerativeAIEmbeddings:
    """
    Create Google embedding model.
    """

    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=GOOGLE_API_KEY,
    )


def create_embedding(
    text: str,
) -> list[float]:
    """
    Convert text into vector embedding.
    """

    embedding_model = get_embedding_model()

    vector = embedding_model.embed_query(
        text
    )

    return vector


def create_embeddings(
    texts: list[str],
) -> list[list[float]]:
    """
    Create embeddings for multiple chunks.
    """

    embedding_model = get_embedding_model()

    vectors = embedding_model.embed_documents(
        texts
    )

    return vectors