"""
state.py

State definition used throughout the LangGraph workflow.
"""

from __future__ import annotations

from typing import Dict
from typing import List
from typing import Optional
from typing import TypedDict


class JobMatchState(TypedDict):
    """
    Shared state for the Resume Job Match Agent.
    """

    # ------------------------------------------------------------------
    # Input Documents
    # ------------------------------------------------------------------

    resume_text: str

    job_description: str

    resume_available: bool

    jd_available: bool

    missing_information: List[str]

    # ------------------------------------------------------------------
    # Parsed Data
    # ------------------------------------------------------------------

    parsed_resume: Optional[Dict]

    parsed_jd: Optional[Dict]

    # ------------------------------------------------------------------
    # Skill Matching
    # ------------------------------------------------------------------

    matched_skills: List[str]

    partially_matched_skills: List[str]

    missing_skills: List[str]

    # ------------------------------------------------------------------
    # Analysis
    # ------------------------------------------------------------------

    gap_analysis: Optional[str]

    fit_score: Optional[int]

    fit_level: Optional[str]

    apply_recommendation: Optional[str]

    resume_improvement_suggestions: Optional[str]

    learning_roadmap: Optional[str]

    # ------------------------------------------------------------------
    # Resume Enhancement
    # ------------------------------------------------------------------

    generated_resume_bullets: Optional[str]

    # ------------------------------------------------------------------
    # Cover Letter
    # ------------------------------------------------------------------

    cover_letter: Optional[str]

    recruiter_message: Optional[str]

   # ------------------------------------------------------------------
   # Human-in-the-Loop Review
   # ------------------------------------------------------------------
    human_review: Optional[Dict]

    workflow_status: Optional[str]

    # ------------------------------------------------------------------
    # Memory
    # ------------------------------------------------------------------

    previous_job_descriptions: List[Dict]

    # ------------------------------------------------------------------
    # Final Output
    # ------------------------------------------------------------------

    final_recommendation: Optional[str]