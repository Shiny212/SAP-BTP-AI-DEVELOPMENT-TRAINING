"""
rag/vector_store.py

In-memory vector storage.
"""

from __future__ import annotations


VECTOR_STORE: list[dict] = []



def add_documents(
    documents: list[dict],
) -> None:
    """
    Store embedded chunks.
    """

    VECTOR_STORE.extend(
        documents
    )



def get_documents() -> list[dict]:
    """
    Return stored documents.
    """

    return VECTOR_STORE