"""
models/schemas.py

Pydantic models for FastAPI requests and responses.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


# =====================================================
# Ingest Request
# =====================================================

class DocumentInput(BaseModel):
    """
    Single document input.
    """

    text: str = Field(
        ...,
        description="Document text"
    )

    source: str = Field(
        ...,
        description="Document source name"
    )


class IngestRequest(BaseModel):
    """
    Request model for /ingest.
    """

    documents: list[DocumentInput]


class IngestResponse(BaseModel):
    """
    Response after ingestion.
    """

    message: str

    chunks_created: int


# =====================================================
# Ask Request
# =====================================================

class QuestionRequest(BaseModel):
    """
    User question.
    """

    question: str


class AnswerResponse(BaseModel):
    """
    RAG answer response.
    """

    answer: str

    sources_used: list[str]