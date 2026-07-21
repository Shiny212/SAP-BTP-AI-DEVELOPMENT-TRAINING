"""
chunker.py

Enterprise Document Chunking Module
for SAP Incident Knowledge Assistant

Responsibilities
----------------
1. Split LangChain Documents into chunks
2. Preserve metadata
3. Configure chunk size and overlap
4. Return chunked documents

Author : Shiny Belsiya
"""

from __future__ import annotations

from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import CHUNK_SIZE, CHUNK_OVERLAP
from src.logger import logger


class DocumentChunker:
    """
    Chunk LangChain Documents for embedding.
    """

    def __init__(
        self,
        chunk_size: int = CHUNK_SIZE,
        chunk_overlap: int = CHUNK_OVERLAP,
    ) -> None:

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                "",
            ],
        )

    def split_documents(
        self,
        documents: List[Document],
    ) -> List[Document]:
        """
        Split documents into chunks.

        Parameters
        ----------
        documents : List[Document]

        Returns
        -------
        List[Document]
        """

        logger.info("Starting document chunking...")

        chunked_documents = self.text_splitter.split_documents(
            documents
        )

        logger.info(
            "Chunking completed. %s chunks created.",
            len(chunked_documents),
        )

        return chunked_documents

    @staticmethod
    def summary(
        chunks: List[Document],
    ) -> None:
        """
        Display chunk statistics.
        """

        print("\n")
        print("=" * 90)
        print("DOCUMENT CHUNK SUMMARY")
        print("=" * 90)

        print(f"Total Chunks : {len(chunks)}")

        if chunks:

            print()

            print("First Chunk Metadata")

            print("-" * 90)

            print(chunks[0].metadata)

            print()

            print("First Chunk Content")

            print("-" * 90)

            print(chunks[0].page_content[:600])

            print()

            print("=" * 90)