"""
nodes/fit_score.py

Fit Score Agent
"""

from __future__ import annotations

from logger import LOGGER
from state import JobMatchState
from tools.fit_score import (
    calculate_fit_score,
    determine_fit_level,
    should_apply,
    score_summary,
)


def fit_score_node(
    state: JobMatchState,
) -> JobMatchState:
    """
    Calculate the overall candidate fit score.

    Scoring Areas
    -------------
    - Core Technical Match
    - SAP BTP Skills
    - GenAI Skills
    - Project Relevance
    - Communication Readiness
    """

    LOGGER.info("Running Fit Score Agent")

    matched_skills = state.get(
        "matched_skills",
        [],
    )

    missing_skills = state.get(
        "missing_skills",
        [],
    )

    parsed_jd = state.get(
        "parsed_jd",
        {},
    )

    required_skills = parsed_jd.get(
        "required_skills",
        [],
    )

    partially_matched_skills = state.get(
        "partially_matched_skills",
        [],
    )

    fit_score = calculate_fit_score(
        matched_skills=matched_skills,
        partially_matched_skills=partially_matched_skills,
        missing_skills=missing_skills,
        required_skills=required_skills,
    )

    fit_level = determine_fit_level(
        fit_score
    )

    apply_recommendation = should_apply(
        fit_score
    )

    summary = score_summary(
        fit_score
    )

    state["fit_score"] = fit_score

    state["fit_level"] = fit_level

    state[
        "apply_recommendation"
    ] = apply_recommendation

    LOGGER.info(
        "Fit Score : %s",
        fit_score,
    )

    LOGGER.info(
        "Fit Level : %s",
        fit_level,
    )

    LOGGER.info(
        "Recommendation : %s",
        apply_recommendation,
    )

    LOGGER.info(
        "Summary : %s",
        summary,
    )

    return state