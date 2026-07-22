"""
feedback/feedback_store.py

In-memory feedback storage.
"""

from __future__ import annotations


FEEDBACK_STORE: list[dict] = []



def add_feedback(
    question: str,
    helpful: bool,
) -> None:
    """
    Store user feedback.
    """

    FEEDBACK_STORE.append(
        {
            "question": question,
            "helpful": helpful,
        }
    )



def get_feedback_summary() -> dict:
    """
    Return feedback counts.
    """

    helpful_count = sum(
        1
        for item in FEEDBACK_STORE
        if item["helpful"]
    )


    not_helpful_count = sum(
        1
        for item in FEEDBACK_STORE
        if not item["helpful"]
    )


    return {
        "helpful": helpful_count,
        "not_helpful": not_helpful_count,
    }