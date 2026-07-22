"""
nodes/resume_bullet_generator.py

Generates ATS-friendly resume bullet points based on the
parsed resume and target job description.
"""

from __future__ import annotations

from config import llm
from logger import LOGGER
from prompts import RESUME_BULLET_GENERATOR_PROMPT
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

                parts.append(
                    item.get(
                        "text",
                        "",
                    )
                )

            elif hasattr(
                item,
                "text",
            ):

                parts.append(
                    item.text
                )

            else:

                parts.append(
                    str(item)
                )

        return "\n".join(
            parts
        ).strip()

    return str(
        content
    ).strip()


def resume_bullet_generator_node(
    state: JobMatchState,
) -> JobMatchState:
    """
    Generate ATS-friendly resume bullet points.
    """

    LOGGER.info(
        "Running Resume Bullet Generator..."
    )

    parsed_resume = state.get(
        "parsed_resume",
        {},
    )

    parsed_jd = state.get(
        "parsed_jd",
        {},
    )

    prompt = RESUME_BULLET_GENERATOR_PROMPT.invoke(
        {
            "resume": parsed_resume,
            "job_description": parsed_jd,
        }
    )

    response = llm.invoke(
        prompt
    )

    bullets = _get_response_text(
        response
    )

    state[
        "generated_resume_bullets"
    ] = bullets

    LOGGER.info(
        "Resume Bullet Generator completed successfully."
    )

    return state