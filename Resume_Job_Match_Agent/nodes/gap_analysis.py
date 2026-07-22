"""
nodes/gap_analysis.py

Gap Analysis Agent
"""

from __future__ import annotations

from config import llm
from logger import LOGGER
from prompts import GAP_ANALYSIS_PROMPT
from state import JobMatchState


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


def gap_analysis_node(
    state: JobMatchState,
) -> JobMatchState:
    """
    Generate a detailed gap analysis.
    """

    LOGGER.info(
        "Running Gap Analysis Agent"
    )

    matched_skills = state.get(
        "matched_skills",
        [],
    )

    missing_skills = state.get(
        "missing_skills",
        [],
    )

    partially_matched_skills = state.get(
        "partially_matched_skills",
        [],
    )

    prompt = GAP_ANALYSIS_PROMPT.invoke(
        {
            "matched": "\n".join(matched_skills),
            "missing": "\n".join(missing_skills),
        }
    )

    response = llm.invoke(prompt)

    analysis = _get_response_text(response)

    if partially_matched_skills:

        analysis += "\n\nPartially Matched Skills\n"
        analysis += "-" * 30 + "\n"

        for skill in partially_matched_skills:
            analysis += f"• {skill}\n"

    if missing_skills:

        analysis += "\nHigh Priority Improvements\n"
        analysis += "-" * 30 + "\n"

        for skill in missing_skills:
            analysis += (
                f"• Gain hands-on experience in {skill} "
                f"and highlight it in your resume.\n"
            )

    if not missing_skills:

        analysis += (
            "\n\nThe resume satisfies all major "
            "technical requirements."
        )

    state["gap_analysis"] = analysis

    LOGGER.info(
        "Gap Analysis completed successfully."
    )

    return state