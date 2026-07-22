"""
models/schemas.py

FastAPI request and response models.
"""

from __future__ import annotations

from pydantic import BaseModel


# =====================================================
# Session Models
# =====================================================


class SessionResponse(BaseModel):
    """
    Response after creating session.
    """

    session_id: str



# =====================================================
# Chat Models
# =====================================================


class ChatRequest(BaseModel):
    """
    User chat request.
    """

    session_id: str

    question: str



class ChatResponse(BaseModel):
    """
    Chat response.
    """

    session_id: str

    answer: str

    sources_used: list[str]



# =====================================================
# History Models
# =====================================================


class Message(BaseModel):
    """
    Single conversation message.
    """

    question: str

    answer: str



class HistoryResponse(BaseModel):
    """
    Conversation history response.
    """

    session_id: str

    messages: list[Message]