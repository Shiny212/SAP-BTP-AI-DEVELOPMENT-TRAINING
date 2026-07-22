"""
models/schemas.py

FastAPI request and response models.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


# ======================================================
# Document Models
# ======================================================

class DocumentInput(BaseModel):
    """
    Single document input.
    """

    text: str = Field(
        ...,
        description="Document content",
    )

    source_name: str = Field(
        ...,
        description="Document file name",
    )

    category: str = Field(
        ...,
        description="Document category",
    )


class IngestRequest(BaseModel):
    """
    Ingest multiple documents.
    """

    documents: list[DocumentInput]


class IngestResponse(BaseModel):
    """
    Ingestion response.
    """

    message: str

    chunks_created: int


# ======================================================
# Question Models
# ======================================================

class QuestionRequest(BaseModel):
    """
    User question with category filter.
    """

    question: str

    category: str


class AnswerResponse(BaseModel):
    """
    Final RAG answer.
    """

    answer: str

    sources_used: list[str]