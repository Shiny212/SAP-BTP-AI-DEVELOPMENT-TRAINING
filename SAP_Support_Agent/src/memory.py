"""
memory.py

Configures LangGraph checkpointing (conversation memory).

Responsibilities:
- Create a reusable InMemorySaver instance
- Provide graph compilation configuration
- Support multi-turn conversations using thread IDs
"""

from __future__ import annotations

from langgraph.checkpoint.memory import InMemorySaver

from src.config import DEFAULT_CONFIG

# ---------------------------------------------------------------------
# LangGraph Checkpointer
# ---------------------------------------------------------------------

# Stores conversation state in memory.
# Can later be replaced with SQLite/Postgres/Redis without changing
# the remaining application code.

checkpointer = InMemorySaver()

# ---------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------

def get_checkpointer() -> InMemorySaver:
    """
    Return the application's checkpointer.

    Returns:
        InMemorySaver instance.
    """
    return checkpointer


def get_graph_config(thread_id: str | None = None) -> dict:
    """
    Return the configuration required by LangGraph.

    Args:
        thread_id:
            Optional conversation thread identifier.

    Returns:
        Configuration dictionary for graph.invoke().
    """

    if thread_id:
        return {
            "configurable": {
                "thread_id": thread_id
            }
        }

    return DEFAULT_CONFIG.copy()


def reset_memory() -> None:
    """
    Placeholder for future memory reset functionality.

    InMemorySaver automatically stores checkpoints during runtime.
    If migrated to persistent storage (SQLite/Postgres),
    this function can be extended to clear saved conversations.
    """
    pass