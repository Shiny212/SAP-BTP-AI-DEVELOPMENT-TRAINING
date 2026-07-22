"""
rag/chunker.py

Document chunking logic.
"""

from __future__ import annotations

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)


def split_document(
    text: str,
) -> list[str]:
    """
    Split document into smaller chunks.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )

    return splitter.split_text(
        text
    )