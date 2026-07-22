"""
nodes/input_validator.py

Validates the user inputs before starting
the LangGraph workflow.
"""

from __future__ import annotations

from state import JobMatchState
from logger import LOGGER


def input_validator_node(
    state: JobMatchState,
) -> JobMatchState:
    """
    Validate resume and job description.

    Returns
    -------
    JobMatchState
    """

    LOGGER.info("Running Input Validator Agent")

    resume_text = state.get(
        "resume_text",
        "",
    ).strip()

    job_description = state.get(
        "job_description",
        "",
    ).strip()

    missing_information: list[str] = []

    resume_available = bool(resume_text)

    jd_available = bool(job_description)

    if not resume_available:
        missing_information.append(
            "Resume is missing."
        )

    if not jd_available:
        missing_information.append(
            "Job Description is missing."
        )

    state["resume_available"] = resume_available

    state["jd_available"] = jd_available

    state["missing_information"] = (
        missing_information
    )

    if missing_information:

        LOGGER.warning(
            "Input validation failed."
        )

    else:

        LOGGER.info(
            "Input validation completed successfully."
        )

    return state