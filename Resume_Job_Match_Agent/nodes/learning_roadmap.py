"""
nodes/learning_roadmap.py

Learning Roadmap Agent
"""

from __future__ import annotations

from config import llm
from logger import LOGGER
from prompts import LEARNING_ROADMAP_PROMPT
from state import JobMatchState
from tools.learning_plan import generate_learning_plan


def _get_response_text(response) -> str:
    """
    Convert LLM response into plain text.
    Supports both string and list-based responses.
    """

    content = response.content

    if isinstance(content, list):
        parts = []

        for item in content:
            if isinstance(item, dict):
                parts.append(item.get("text", ""))
            elif hasattr(item, "text"):
                parts.append(item.text)
            else:
                parts.append(str(item))

        return "\n".join(parts).strip()

    return str(content).strip()


def learning_roadmap_node(
    state: JobMatchState,
) -> JobMatchState:
    """
    Generate a personalized learning roadmap
    for the missing skills.
    """

    LOGGER.info(
        "Running Learning Roadmap Agent"
    )

    missing_skills = state.get(
        "missing_skills",
        [],
    )

    # ---------------------------------------
    # Rule-based Learning Plan
    # ---------------------------------------

    roadmap = generate_learning_plan(
        missing_skills
    )

    # ---------------------------------------
    # LLM Enhanced Roadmap
    # ---------------------------------------

    prompt = LEARNING_ROADMAP_PROMPT.invoke(
        {
            "missing": "\n".join(
                missing_skills
            )
        }
    )

    response = llm.invoke(
        prompt
    )

    ai_plan = _get_response_text(
        response
    )

    final_plan = (
        roadmap
        + "\n\n"
        + "=" * 80
        + "\n"
        + "LLM RECOMMENDATIONS"
        + "\n"
        + "=" * 80
        + "\n\n"
        + ai_plan
    )

    state["learning_roadmap"] = final_plan

    LOGGER.info(
        "Learning Roadmap generated successfully."
    )

    return state