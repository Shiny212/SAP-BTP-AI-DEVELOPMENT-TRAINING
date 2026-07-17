"""
vector_store.py

Enterprise Chroma Vector Store Manager

Responsibilities
----------------
1. Create persistent ChromaDB
2. Load existing database
3. Add documents
4. Similarity search
5. Delete database
6. Database statistics

Author : Shiny Belsiya
"""

from __future__ import annotations

import shutil
import time

from google.api_core.exceptions import ResourceExhausted
from pathlib import Path
from typing import List


from langchain_chroma import Chroma
from langchain_core.documents import Document


from src.config import (
    CHROMA_DB_PATH,
    COLLECTION_NAME,
    EMBEDDING_BATCH_SIZE,
    MAX_RETRIES,
    RETRY_WAIT_SECONDS,
)
from src.embeddings import EmbeddingService
from src.logger import logger


class VectorStoreManager:
    """
    Chroma Vector Store Manager.
    """

    def __init__(self) -> None:

        self.embedding_model = (
            EmbeddingService.get_embeddings()
        )

        self.persist_directory = str(CHROMA_DB_PATH)

        self.collection_name = COLLECTION_NAME

        self.vector_store: Chroma | None = None

    # ---------------------------------------------------------

    def database_exists(self) -> bool:
        """
        Check whether Chroma database exists.
        """

        path = Path(self.persist_directory)
        return (
            path.exists()
            and path.is_dir()
            and any(path.iterdir())
        )

    # ---------------------------------------------------------

    def create(
        self,
        documents: List[Document],
    ) -> Chroma:
        """
        Create Chroma database in batches.
        """

        logger.info("Creating Chroma Vector Store...")

        batch_size = EMBEDDING_BATCH_SIZE

        # First batch creates the database
        first_batch = documents[:batch_size]

        self.vector_store = Chroma.from_documents(
            documents=first_batch,
            embedding=self.embedding_model,
            persist_directory=self.persist_directory,
            collection_name=self.collection_name,
        )

        logger.info(
            "Batch 1/%s completed.",
            (len(documents) + batch_size - 1) // batch_size,
        )

        # Remaining batches
        for start in range(batch_size, len(documents), batch_size):

            end = min(start + batch_size, len(documents))

            batch = documents[start:end]

            retries = 0

            while retries < MAX_RETRIES:

                try:
                    if self.vector_store is None:
                        raise RuntimeError(
                            "Vector Store was not initialized."
                        )

                    self.vector_store.add_documents(batch)

                    logger.info(
                        "Batch %s-%s inserted successfully.",
                        start + 1,
                        end,
                    )

                    break
                except Exception as error:
                    error_message = str(error)

                    if (
                        "RESOURCE_EXHAUSTED" in error_message
                        or "429" in error_message
                    ):
                        retries += 1

                        logger.warning(
                            "Gemini quota exceeded. Retry %s/%s after %s seconds...",
                            retries,
                            MAX_RETRIES,
                            RETRY_WAIT_SECONDS,
                        )

                        logger.debug(error_message)

                        time.sleep(RETRY_WAIT_SECONDS)

                        continue

                    raise
            else:
                raise RuntimeError(
                    f"Failed to embed batch "
                    f"{start + 1}-{end} "
                    f"after {MAX_RETRIES} retries."
                )

        logger.info("Vector Store Created Successfully.")

        return self.vector_store

    # ---------------------------------------------------------

    def load(self) -> Chroma:
        """
        Load an existing vector database.
        """

        logger.info("Loading Chroma Vector Store...")

        self.vector_store = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embedding_model,
            collection_name=self.collection_name,
        )

        logger.info(
            "Vector Store loaded successfully."
        )

        return self.vector_store

    # ---------------------------------------------------------

    def get_or_create(
        self,
        documents: List[Document],
    ) -> Chroma:
        """
        Load existing database or create a new one.
        """

        if self.database_exists():

            return self.load()

        return self.create(documents)

    # ---------------------------------------------------------

    def similarity_search(
        self,
        query: str,
        k: int = 5,
        filter: dict | None = None,
    ) -> List[Document]:
        """
        Retrieve similar documents with optional metadata filtering.
        """

        if self.vector_store is None:
            raise RuntimeError("Vector Store has not been initialized.")

        logger.info("Running similarity search...")

        if filter:
            logger.info("Applying Metadata Filter: %s", filter)

        return self.vector_store.similarity_search(
            query=query,
            k=k,
            filter=filter,
        )

    # ---------------------------------------------------------

    def similarity_search_with_score(
        self,
        query: str,
        k: int = 5,
        filter: dict | None = None,
    ) -> List[tuple[Document, float]]:
        """
        Retrieve similar documents with scores and optional metadata filtering.
        """

        if self.vector_store is None:
            raise RuntimeError(
                "Vector Store has not been initialized."
            )

        if filter:
            logger.info(
                "Applying Metadata Filter: %s",
                filter,
            )

        return self.vector_store.similarity_search_with_score(
            query=query,
            k=k,
            filter=filter,
        )

    # ---------------------------------------------------------

    def delete_database(self) -> None:
        """
        Delete Chroma database.
        """

        path = Path(self.persist_directory)

        if path.exists():

            shutil.rmtree(path)

            logger.info(
                "Existing Vector Database Deleted."
            )

    # ---------------------------------------------------------

    def count(self) -> int:
        """
        Return total vectors.
        """

        if self.vector_store is None:

            raise RuntimeError(
                "Vector Store has not been initialized."
            )

        collection = self.vector_store.get()

        return len(collection["ids"])