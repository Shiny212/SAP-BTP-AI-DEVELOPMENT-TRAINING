"""
memory/session_memory.py

In-memory conversation storage.
"""

from __future__ import annotations


import uuid



# =====================================================
# Session Storage
# =====================================================

SESSION_MEMORY: dict[str, list[dict]] = {}



def create_session() -> str:
    """
    Create a new unique session.
    """

    session_id = str(
        uuid.uuid4()
    )


    SESSION_MEMORY[session_id] = []


    return session_id



def get_history(
    session_id: str,
) -> list[dict]:
    """
    Get conversation history.
    """

    return SESSION_MEMORY.get(
        session_id,
        [],
    )



def add_message(
    session_id: str,
    question: str,
    answer: str,
) -> None:
    """
    Store question and answer.
    """

    if session_id not in SESSION_MEMORY:

        SESSION_MEMORY[session_id] = []


    SESSION_MEMORY[session_id].append(
        {
            "question": question,
            "answer": answer,
        }
    )