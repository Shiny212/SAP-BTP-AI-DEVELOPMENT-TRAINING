"""
nodes/skill_matcher.py

Production Ready Skill Matching Agent
"""

from __future__ import annotations

from difflib import SequenceMatcher

from logger import LOGGER
from state import JobMatchState
from tools.skill_normalizer import (
    normalize_skill,
    normalize_skill_list,
)

# ==========================================================
# CONFIGURATION
# ==========================================================

# Lower threshold improves matching for:
# Gemini <-> Gemini API
# SAP HANA <-> SAP HANA Cloud
# REST API <-> RESTful API

FUZZY_MATCH_THRESHOLD = 0.75


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def _normalize(skill: str) -> str:
    """
    Normalize a skill for comparison.
    """

    return normalize_skill(skill).strip().lower()


def _similarity(
    skill_a: str,
    skill_b: str,
) -> float:
    """
    Calculate similarity between two skills.
    """

    return SequenceMatcher(
        None,
        _normalize(skill_a),
        _normalize(skill_b),
    ).ratio()


def _is_exact_match(
    resume_skill: str,
    jd_skill: str,
) -> bool:
    """
    Exact comparison.
    """

    return _normalize(resume_skill) == _normalize(jd_skill)


def _is_partial_match(
    resume_skill: str,
    jd_skill: str,
) -> bool:
    """
    Partial comparison.

    Examples:

    SAP HANA
    SAP HANA Cloud

    REST API
    RESTful API

    Avoids false matches like:

    C -> Communication
    C -> CI/CD
    """

    resume = _normalize(resume_skill)

    jd = _normalize(jd_skill)


    if resume == jd:
        return False


    # Avoid single character matching
    if len(resume) <= 2:
        return False


    if resume in jd:
        return True


    if jd in resume:
        return True


    resume_words = set(
        resume.split()
    )

    jd_words = set(
        jd.split()
    )


    common_words = (
        resume_words &
        jd_words
    )


    for word in common_words:

        # Ignore very small words
        if len(word) >= 3:
            return True


    return False

def _is_fuzzy_match(
    resume_skill: str,
    jd_skill: str,
) -> bool:
    """
    Fuzzy comparison.
    """

    return (
        _similarity(
            resume_skill,
            jd_skill,
        )
        >= FUZZY_MATCH_THRESHOLD
    )


def _match_type(
    resume_skill: str,
    jd_skill: str,
) -> str | None:
    """
    Determine match type.
    """

    if _is_exact_match(
        resume_skill,
        jd_skill,
    ):
        return "exact"

    if _is_partial_match(
        resume_skill,
        jd_skill,
    ):
        return "partial"

    if _is_fuzzy_match(
        resume_skill,
        jd_skill,
    ):
        return "fuzzy"

    return None
# ==========================================================
# MAIN SKILL MATCHER
# ==========================================================

def skill_matching_node(
    state: JobMatchState,
) -> JobMatchState:
    """
    Compare resume skills with
    job description skills.
    """

    LOGGER.info(
        "Running Skill Matching Agent"
    )

    resume = state["parsed_resume"]
    jd = state["parsed_jd"]

    # ------------------------------------------------------
    # Normalize Skills
    # ------------------------------------------------------

    resume_skills = normalize_skill_list(
        resume.get(
            "core_skills",
            [],
        )
    )

    required_skills = normalize_skill_list(
        jd.get(
            "required_skills",
            [],
        )
    )

    preferred_skills = normalize_skill_list(
        jd.get(
            "preferred_skills",
            [],
        )
    )

    job_skills = sorted(
        set(
            required_skills +
            preferred_skills
        ),
        key=str.lower,
    )

    # ------------------------------------------------------
    # Debug Logs
    # ------------------------------------------------------

    LOGGER.info(
        "Resume Skills (%d): %s",
        len(resume_skills),
        resume_skills,
    )

    LOGGER.info(
        "Required Skills (%d): %s",
        len(required_skills),
        required_skills,
    )

    LOGGER.info(
        "Preferred Skills (%d): %s",
        len(preferred_skills),
        preferred_skills,
    )

    LOGGER.info(
        "Total Job Skills (%d): %s",
        len(job_skills),
        job_skills,
    )

    # ------------------------------------------------------
    # Match Containers
    # ------------------------------------------------------

    matched = set()
    partial = set()
    missing = set()

    match_details = []

    # ------------------------------------------------------
    # Matching Logic
    # ------------------------------------------------------

    for jd_skill in job_skills:

        found = False

        for resume_skill in resume_skills:

            match = _match_type(
                resume_skill,
                jd_skill,
            )

            if match is None:
                continue

            found = True

            if match == "exact":

                matched.add(jd_skill)

            elif match == "partial":

                partial.add(jd_skill)

            elif match == "fuzzy":

                matched.add(jd_skill)

            match_details.append(
                {
                    "resume_skill": resume_skill,
                    "jd_skill": jd_skill,
                    "match_type": match,
                    "similarity": round(
                        _similarity(
                            resume_skill,
                            jd_skill,
                        ),
                        2,
                    ),
                }
            )

            break

        if not found:

            missing.add(jd_skill)

    # ------------------------------------------------------
    # Remove Overlaps
    # ------------------------------------------------------

    partial -= matched

    missing -= matched

    missing -= partial

    # ------------------------------------------------------
    # Save Results
    # ------------------------------------------------------

    state["matched_skills"] = sorted(
        matched,
        key=str.lower,
    )

    state["partially_matched_skills"] = sorted(
        partial,
        key=str.lower,
    )

    state["missing_skills"] = sorted(
        missing,
        key=str.lower,
    )

    state["skill_match_details"] = match_details

    # ------------------------------------------------------
    # Logs
    # ------------------------------------------------------

    LOGGER.info(
        "Matched Skills : %d",
        len(state["matched_skills"]),
    )

    LOGGER.info(
        "Partial Skills : %d",
        len(state["partially_matched_skills"]),
    )

    LOGGER.info(
        "Missing Skills : %d",
        len(state["missing_skills"]),
    )

    LOGGER.info(
        "Match Details:"
    )

    for item in match_details:

        LOGGER.info(
            "%s  <--->  %s (%s | %.2f)",
            item["resume_skill"],
            item["jd_skill"],
            item["match_type"],
            item["similarity"],
        )

    LOGGER.info(
        "Skill Matching completed successfully."
    )

    return state