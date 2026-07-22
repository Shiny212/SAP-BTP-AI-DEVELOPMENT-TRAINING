"""
rag/vector_store.py

In-memory vector storage.
"""

from __future__ import annotations


# In-memory vector database
VECTOR_STORE: list[dict] = []


def add_documents(
    documents: list[dict],
) -> None:
    """
    Store document chunks and embeddings
    in memory.
    """

    VECTOR_STORE.extend(
        documents
    )


def get_all_documents() -> list[dict]:
    """
    Return all stored documents.
    """

    return VECTOR_STORE


def clear_store() -> None:
    """
    Clear memory storage.
    """

    VECTOR_STORE.clear()