"""
models.py

Pydantic Models
"""

from typing import Literal

from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
)


class SupportTicket(BaseModel):
    """
    Structured customer support ticket.
    """

    # Reject unexpected fields returned by the LLM
    model_config = ConfigDict(
        extra="forbid"
    )

    category: Literal[
        "Billing",
        "Technical",
        "Account",
        "Delivery",
        "Order",
        "Refund",
        "Other"
    ] = Field(
        description="Category of the customer request."
    )

    priority: Literal[
        "High",
        "Medium",
        "Low"
    ] = Field(
        description="Priority of the request."
    )

    sentiment: Literal[
        "Positive",
        "Neutral",
        "Negative"
    ] = Field(
        description="Customer sentiment."
    )

    summary: str = Field(
        min_length=5,
        max_length=200,
        description="Short summary of the request."
    )

    recommended_team: str = Field(
        min_length=3,
        max_length=100,
        description="Recommended support team."
    )

    requires_human_agent: bool = Field(
        description="Whether escalation is required."
    )

    route: Literal[
        "TOOL",
        "RAG",
        "LLM"
    ] = Field(
        description="Execution route selected for this request."
    )