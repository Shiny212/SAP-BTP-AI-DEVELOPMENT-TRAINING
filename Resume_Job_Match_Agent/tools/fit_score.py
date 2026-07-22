"""
tools/fit_score.py

Production Ready Candidate Fit Score Calculator
"""

from __future__ import annotations

from typing import List
from math import ceil


# ==========================================================
# SCORE WEIGHTS
# ==========================================================

CORE_SKILL_WEIGHT = 50
PARTIAL_SKILL_WEIGHT = 15
SAP_BTP_WEIGHT = 15
GENAI_WEIGHT = 10
PROJECT_WEIGHT = 5
READINESS_WEIGHT = 5


# ==========================================================
# SAP SKILLS
# ==========================================================

SAP_BTP_SKILLS = {
    "SAP BTP",
    "SAP AI Core",
    "SAP Generative AI Hub",
    "SAP Joule",
    "SAP CAP",
    "Cloud Application Programming Model",
    "SAP Integration Suite",
    "SAP HANA Cloud",
    "SAP Build",
    "SAP Build Apps",
    "SAP Build Process Automation",
    "SAP Workflow Management",
    "ABAP Cloud",
    "RAP",
}


# ==========================================================
# GENERATIVE AI SKILLS
# ==========================================================

GENAI_SKILLS = {
    "LangChain",
    "LangGraph",
    "RAG",
    "GraphRAG",
    "Prompt Engineering",
    "Vector Database",
    "Agentic AI",
}


# ==========================================================
# PROJECT RELATED SKILLS
# ==========================================================

PROJECT_SKILLS = {
    "Python",
    "Machine Learning",
    "Deep Learning",
    "Streamlit",
    "Pandas",
    "TensorFlow",
    "Scikit-Learn",
    "YOLO",
    "Computer Vision",
    "OpenCV",
    "IoT",
    "REST API",
    "LangGraph",
    "RAG",
}


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def _percentage(
    matched: float,
    total: int,
) -> float:
    """
    Return percentage.
    """

    if total <= 0:
        return 0.0

    return matched / total


def _calculate_weight(
    matched: float,
    total: int,
    weight: int,
) -> int:
    """
    Calculate weighted score.
    """

    value = _percentage(
        matched,
        total,
    ) * weight

    return ceil(value)


# ==========================================================
# CORE SCORE
# ==========================================================

def _core_skill_score(
    matched_skills: List[str],
    partially_matched_skills: List[str],
    required_skills: List[str],
) -> int:
    """
    Core technical score.

    Partial skills contribute
    50 percent of an exact match.
    """

    exact = len(
        set(matched_skills)
        &
        set(required_skills)
    )

    partial = len(
        set(partially_matched_skills)
        &
        set(required_skills)
    )

    effective_match = exact + (partial * 0.5)

    return _calculate_weight(
        matched=effective_match,
        total=max(len(required_skills), 1),
        weight=CORE_SKILL_WEIGHT,
    )


# ==========================================================
# SAP SCORE
# ==========================================================

def _sap_score(
    matched_skills: List[str],
    partially_matched_skills: List[str],
    required_skills: List[str],
) -> int:
    """
    SAP BTP score.
    """

    required = (
        set(required_skills)
        &
        SAP_BTP_SKILLS
    )

    exact = (
        set(matched_skills)
        &
        required
    )

    partial = (
        set(partially_matched_skills)
        &
        required
    )

    effective = len(exact) + (
        len(partial) * 0.5
    )

    return _calculate_weight(
        effective,
        max(len(required), 1),
        SAP_BTP_WEIGHT,
    )


# ==========================================================
# GENERATIVE AI SCORE
# ==========================================================

def _genai_score(
    matched_skills: List[str],
    partially_matched_skills: List[str],
    required_skills: List[str],
) -> int:
    """
    GenAI score.
    """

    required = (
        set(required_skills)
        &
        GENAI_SKILLS
    )

    exact = (
        set(matched_skills)
        &
        required
    )

    partial = (
        set(partially_matched_skills)
        &
        required
    )

    effective = len(exact) + (
        len(partial) * 0.5
    )

    return _calculate_weight(
        effective,
        max(len(required), 1),
        GENAI_WEIGHT,
    )


# ==========================================================
# PROJECT SCORE
# ==========================================================

def _project_score(
    matched_skills: List[str],
) -> int:
    """
    Project relevance score.
    """

    matches = (
        set(matched_skills)
        &
        PROJECT_SKILLS
    )

    return _calculate_weight(
        len(matches),
        len(PROJECT_SKILLS),
        PROJECT_WEIGHT,
    )


# ==========================================================
# READINESS SCORE
# ==========================================================

def _readiness_score(
    missing_skills: List[str],
) -> int:
    """
    Candidate readiness score.
    """

    missing = len(missing_skills)

    if missing <= 2:
        return 5

    if missing <= 5:
        return 4

    if missing <= 8:
        return 3

    if missing <= 12:
        return 2

    return 1
# ==========================================================
# MAIN FIT SCORE CALCULATOR
# ==========================================================

def calculate_fit_score(
    matched_skills: List[str],
    partially_matched_skills: List[str],
    missing_skills: List[str],
    required_skills: List[str],
) -> int:
    """
    Calculate the overall candidate fit score.

    Score Distribution
    ------------------
    Core Technical Skills : 50
    Partial Skills        : Included in core (50% weight)
    SAP Skills            : 15
    GenAI Skills          : 10
    Project Relevance     : 5
    Readiness             : 5

    Total                 : 85

    The remaining 15 points are awarded as a consistency bonus
    for candidates with strong overall matching.
    """

    core = _core_skill_score(
        matched_skills,
        partially_matched_skills,
        required_skills,
    )

    sap = _sap_score(
        matched_skills,
        partially_matched_skills,
        required_skills,
    )

    genai = _genai_score(
        matched_skills,
        partially_matched_skills,
        required_skills,
    )

    project = _project_score(
        matched_skills,
    )

    readiness = _readiness_score(
        missing_skills,
    )

    total = (
        core
        + sap
        + genai
        + project
        + readiness
    )

    # ======================================================
    # Consistency Bonus
    # ======================================================

    required_count = max(len(required_skills), 1)

    effective_match = (
        len(matched_skills)
        + (0.5 * len(partially_matched_skills))
    )

    overall_percentage = (
        effective_match / required_count
    ) * 100

    if overall_percentage >= 90:
        total += 15

    elif overall_percentage >= 80:
        total += 12

    elif overall_percentage >= 70:
        total += 10

    elif overall_percentage >= 60:
        total += 8

    elif overall_percentage >= 50:
        total += 6

    elif overall_percentage >= 40:
        total += 4

    elif overall_percentage >= 30:
        total += 2

    return min(round(total), 100)


# ==========================================================
# FIT LEVEL
# ==========================================================

def determine_fit_level(
    score: int,
) -> str:
    """
    Determine candidate fit level.
    """

    if score >= 90:
        return "Excellent Fit"

    if score >= 75:
        return "Strong Fit"

    if score >= 60:
        return "Good Fit"

    if score >= 45:
        return "Moderate Fit"

    if score >= 30:
        return "Weak Fit"

    return "Poor Fit"


# ==========================================================
# APPLICATION RECOMMENDATION
# ==========================================================

def should_apply(
    score: int,
) -> str:
    """
    Recommendation based on score.
    """

    if score >= 90:
        return "Definitely Apply"

    if score >= 75:
        return "Apply"

    if score >= 60:
        return "Apply after minor resume improvements"

    if score >= 45:
        return "Improve resume and apply"

    if score >= 30:
        return "Upskill before applying"

    return "Do not apply now"


# ==========================================================
# MATCH PERCENTAGE
# ==========================================================

def calculate_match_percentage(
    matched_skills: List[str],
    partially_matched_skills: List[str],
    required_skills: List[str],
) -> float:
    """
    Calculate effective match percentage.

    Partial matches count as 50%.
    """

    if not required_skills:
        return 0.0

    effective = (
        len(matched_skills)
        + (0.5 * len(partially_matched_skills))
    )

    percentage = (
        effective
        / len(required_skills)
    ) * 100

    return round(
        percentage,
        2,
    )


# ==========================================================
# SCORE SUMMARY
# ==========================================================

def score_summary(
    fit_score: int,
) -> dict:
    """
    Return score summary.
    """

    return {
        "fit_score": fit_score,
        "fit_level": determine_fit_level(
            fit_score
        ),
        "recommendation": should_apply(
            fit_score
        ),
    }