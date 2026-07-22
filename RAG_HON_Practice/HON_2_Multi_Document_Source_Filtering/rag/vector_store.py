"""
rag/vector_store.py

In-memory vector storage with metadata.
"""

from __future__ import annotations


VECTOR_STORE: list[dict] = []


def add_documents(
    documents: list[dict],
) -> None:
    """
    Store document chunks in memory.
    """

    VECTOR_STORE.extend(
        documents
    )


def get_documents_by_category(
    category: str,
) -> list[dict]:
    """
    Filter documents using category.
    """

    return [
        document
        for document in VECTOR_STORE
        if document["category"].lower()
        == category.lower()
    ]


def get_all_documents() -> list[dict]:
    """
    Return all stored documents.
    """

    return VECTOR_STORE