"""
schemas.py

Request and Response Models

Author : Shiny Belsiya
"""

from pydantic import BaseModel


class QuestionRequest(BaseModel):
    question: str


class QuestionResponse(BaseModel):
    answer: str