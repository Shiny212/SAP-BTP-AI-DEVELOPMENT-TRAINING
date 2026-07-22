"""
rag/chunker.py

Document chunking logic.
"""

from __future__ import annotations

from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_document(
    text: str,
) -> list[str]:
    """
    Split long documents into smaller chunks.

    Returns:
        List of text chunks.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )

    chunks = splitter.split_text(
        text
    )

    return chunks