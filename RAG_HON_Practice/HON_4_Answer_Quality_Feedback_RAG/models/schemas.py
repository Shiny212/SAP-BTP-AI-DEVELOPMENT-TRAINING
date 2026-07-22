"""
models/schemas.py

FastAPI request and response models.
"""

from __future__ import annotations

from pydantic import BaseModel


# =====================================================
# Ingest Models
# =====================================================

class IngestRequest(BaseModel):
    """
    Document ingestion request.
    """

    text: str

    source_name: str



class IngestResponse(BaseModel):
    """
    Ingestion response.
    """

    message: str

    chunks_created: int



# =====================================================
# Question Models
# =====================================================

class AskRequest(BaseModel):
    """
    Question request.
    """

    question: str



class AskResponse(BaseModel):
    """
    Answer with quality check.
    """

    answer: str

    supported_by_documents: bool

    confidence: str

    sources_used: list[str]



# =====================================================
# Feedback Models
# =====================================================

class FeedbackRequest(BaseModel):
    """
    User feedback request.
    """

    question: str

    helpful: bool



class FeedbackSummaryResponse(BaseModel):
    """
    Feedback summary.
    """

    helpful: int

    not_helpful: int