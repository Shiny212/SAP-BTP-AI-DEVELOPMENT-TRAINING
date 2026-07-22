"""
nodes/cover_letter.py

Cover Letter Generator Agent
"""

from __future__ import annotations

from config import llm
from logger import LOGGER
from prompts import (
    COVER_LETTER_PROMPT,
    RECRUITER_MESSAGE_PROMPT,
)
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


def cover_letter_node(
    state: JobMatchState,
) -> JobMatchState:
    """
    Generate a professional cover letter
    and recruiter message.
    """

    LOGGER.info(
        "Running Cover Letter Generator Agent"
    )

    resume_text = state.get(
        "resume_text",
        "",
    )

    job_description = state.get(
        "job_description",
        "",
    )

    # ----------------------------------------
    # Cover Letter
    # ----------------------------------------

    cover_prompt = COVER_LETTER_PROMPT.invoke(
        {
            "resume": resume_text,
            "job_description": job_description,
        }
    )

    cover_response = llm.invoke(
        cover_prompt
    )

    cover_letter = _get_response_text(
        cover_response
    )

    # ----------------------------------------
    # Recruiter Message
    # ----------------------------------------

    recruiter_prompt = (
        RECRUITER_MESSAGE_PROMPT.invoke(
            {
                "resume": resume_text,
                "job_description": job_description,
            }
        )
    )

    recruiter_response = llm.invoke(
        recruiter_prompt
    )

    recruiter_message = _get_response_text(
        recruiter_response
    )

    state["cover_letter"] = (
        cover_letter
    )

    state["recruiter_message"] = (
        recruiter_message
    )

    LOGGER.info(
        "Cover Letter generated successfully."
    )

    LOGGER.info(
        "Recruiter Message generated successfully."
    )

    return state