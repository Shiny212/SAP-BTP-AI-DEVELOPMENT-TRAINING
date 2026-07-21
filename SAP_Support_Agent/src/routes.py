"""
routes.py

Routing functions for the SAP Support Agent LangGraph workflow.
"""

from __future__ import annotations

from typing import Literal

from src.state import SupportAgentState


def route_after_classification(
    state: SupportAgentState,
) -> Literal["priority"]:
    """
    Route to the priority assignment node.
    """
    return "priority"


def route_after_priority(
    state: SupportAgentState,
) -> Literal["draft"]:
    """
    Route to the draft response node.
    """
    return "draft"


def route_after_review(
    state: SupportAgentState,
) -> Literal["final", "draft"]:
    """
    Decide whether the draft is approved or should be regenerated.
    """

    approval_status = (
        state.get("approval_status", "Approved")
        .strip()
        .lower()
    )

    if approval_status == "approved":
        return "final"

    return "draft"


def route_after_final(
    state: SupportAgentState,
) -> Literal["post_process"]:
    """
    Route to post-processing.
    """
    return "post_process"