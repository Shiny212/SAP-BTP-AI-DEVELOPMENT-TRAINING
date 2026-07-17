"""
retriever.py

Enterprise Retriever Module

Responsibilities
----------------
1. Create LangChain Retriever
2. Retrieve relevant documents
3. Similarity Search
4. Metadata Search
5. Pretty Printing

Author : Shiny Belsiya
"""

from __future__ import annotations

from typing import List

from langchain_core.documents import Document

from src.config import (
    DEFAULT_TOP_K,
    MAX_TOP_K,
)
from src.logger import logger
from src.vector_store import VectorStoreManager


class SAPIncidentRetriever:
    """
    Enterprise Retriever for SAP Incident RAG.
    """

    def __init__(self) -> None:

        self.vector_store = VectorStoreManager()

    # ---------------------------------------------------------

    def initialize(
        self,
        documents: List[Document],
    ) -> None:
        """
        Load or create vector database.
        """

        self.vector_store.get_or_create(documents)

    # ---------------------------------------------------------

    def retrieve(
        self,
        query: str,
        k: int = DEFAULT_TOP_K,
    ) -> List[Document]:
        """
        Retrieve top-k similar documents.
        """

        if k > MAX_TOP_K:
            k = MAX_TOP_K

        logger.info(
            "Retrieving Top-%s documents...",
            k,
        )

        return self.vector_store.similarity_search(
            query=query,
            k=k,
        )

    # ---------------------------------------------------------

    def retrieve_with_score(
        self,
        query: str,
        k: int = DEFAULT_TOP_K,
    ):
        if k > MAX_TOP_K:
            k = MAX_TOP_K

        logger.info(
            "Retrieving documents with similarity score..."
        )

        return self.vector_store.similarity_search_with_score(
            query=query,
            k=k,
        )

    # ---------------------------------------------------------

    @staticmethod
    def show_documents(
        documents: List[Document],
    ) -> None:
        """
        Pretty print retrieved documents.
        """

        print("\n")
        print("=" * 90)
        print("RETRIEVED DOCUMENTS")
        print("=" * 90)

        for rank, document in enumerate(
            documents,
            start=1,
        ):

            print(f"\nRank #{rank}")

            print("-" * 90)

            print(document.page_content)

            print()

            print("Metadata")

            print(document.metadata)

            print("=" * 90)

    # ---------------------------------------------------------

    @staticmethod
    def show_documents_with_score(
        documents,
    ) -> None:
        """
        Pretty print retrieved documents with scores.
        """

        print("\n")
        print("=" * 90)
        print("RETRIEVED DOCUMENTS WITH SCORE")
        print("=" * 90)

        for rank, (document, score) in enumerate(
            documents,
            start=1,
        ):

            print(f"\nRank #{rank}")

            print(f"Similarity Score : {score:.4f}")

            print("-" * 90)

            print(document.page_content)

            print()

            print("Metadata")

            print(document.metadata)

            print("=" * 90)