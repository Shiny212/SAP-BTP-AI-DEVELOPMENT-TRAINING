"""
nodes/final_recommendation.py

Final Recommendation Agent
"""

from __future__ import annotations

from config import llm
from logger import LOGGER
from prompts import FINAL_RECOMMENDATION_PROMPT
from state import JobMatchState
from tools.memory import (
    save_memory,
)


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


def final_recommendation_node(
    state: JobMatchState,
) -> JobMatchState:
    """
    Generate the final candidate report.
    """

    LOGGER.info(
        "Running Final Recommendation Agent"
    )

    fit_score = state.get(
        "fit_score",
        0,
    )

    fit_level = state.get(
        "fit_level",
        "",
    )

    matched_skills = state.get(
        "matched_skills",
        [],
    )

    missing_skills = state.get(
        "missing_skills",
        [],
    )

    gap_analysis = state.get(
        "gap_analysis",
        "",
    )

    resume_suggestions = state.get(
        "resume_improvement_suggestions",
        "",
    )

    learning_plan = state.get(
        "learning_roadmap",
        "",
    )

    apply_recommendation = state.get(
        "apply_recommendation",
        "",
    )

    cover_letter = state.get(
        "cover_letter",
        "",
    )

    recruiter_message = state.get(
        "recruiter_message",
        "",
    )

    generated_bullets = state.get(
        "generated_resume_bullets",
        "",
    )

    previous_jobs = state.get(
        "previous_job_descriptions",
        [],
    )

    prompt = FINAL_RECOMMENDATION_PROMPT.invoke(
        {
            "fit_score": fit_score,
            "fit_level": fit_level,
            "matched": "\n".join(
                matched_skills
            ),
            "missing": "\n".join(
                missing_skills
            ),
            "gap_analysis": gap_analysis,
            "resume_suggestions": resume_suggestions,
            "learning_plan": learning_plan,
        }
    )

    response = llm.invoke(
        prompt
    )

    llm_report = _get_response_text(
        response
    )

    report = []

    report.append("=" * 80)
    report.append(
        "CANDIDATE FIT REPORT"
    )
    report.append("=" * 80)
    report.append("")

    report.append(
        f"Fit Score : {fit_score}/100"
    )

    report.append(
        f"Fit Level : {fit_level}"
    )

    report.append(
        f"Recommendation : {apply_recommendation}"
    )

    report.append("")

    report.append("=" * 80)
    report.append("MATCHED SKILLS")
    report.append("=" * 80)

    if matched_skills:

        for skill in matched_skills:

            report.append(
                f"• {skill}"
            )

    else:

        report.append(
            "None"
        )

    report.append("")

    report.append("=" * 80)
    report.append("MISSING SKILLS")
    report.append("=" * 80)

    if missing_skills:

        for skill in missing_skills:

            report.append(
                f"• {skill}"
            )

    else:

        report.append(
            "None"
        )

    report.append("")

    report.append("=" * 80)
    report.append(
        "GAP ANALYSIS"
    )
    report.append("=" * 80)
    report.append(
        gap_analysis
    )
    report.append("")

    if resume_suggestions:

        report.append("=" * 80)
        report.append(
            "RESUME IMPROVEMENT"
        )
        report.append("=" * 80)
        report.append(
            resume_suggestions
        )
        report.append("")

    if learning_plan:

        report.append("=" * 80)
        report.append(
            "LEARNING ROADMAP"
        )
        report.append("=" * 80)
        report.append(
            learning_plan
        )
        report.append("")

    if state.get(
        "human_approval",
        False,
    ):

        report.append("=" * 80)
        report.append(
            "COVER LETTER"
        )
        report.append("=" * 80)
        report.append(
            cover_letter
        )
        report.append("")

        report.append("=" * 80)
        report.append(
            "RECRUITER MESSAGE"
        )
        report.append("=" * 80)
        report.append(
            recruiter_message
        )
        report.append("")

    if previous_jobs:

        report.append("=" * 80)
        report.append(
            "PREVIOUS ANALYSES"
        )
        report.append("=" * 80)

        for job in previous_jobs[-5:]:

            report.append(
                f"Job Title      : {job.get('job_title', 'Unknown Job')}"
            )

            report.append(
                f"Fit Score      : {job.get('fit_score', 0)}/100"
            )

            report.append(
                f"Recommendation : {job.get('recommendation', 'N/A')}"
            )

            report.append(
                "-" * 40
            )

        report.append("")

    if generated_bullets:

        report.append("=" * 80)
        report.append(
            "ATS RESUME BULLET SUGGESTIONS"
        )
        report.append("=" * 80)
        report.append(
            generated_bullets
        )
        report.append("")

    report.append("=" * 80)
    report.append(
        "LLM CAREER ADVISOR SUMMARY"
    )
    report.append("=" * 80)
    report.append(
        llm_report
    )

    state["final_recommendation"] = "\n".join(
        report
    )

    save_memory(
        job_title=state.get(
            "parsed_jd",
            {},
        ).get(
            "job_title",
            "Unknown Job",
        ),
        fit_score=fit_score,
        recommendation=apply_recommendation,
    )

    LOGGER.info(
        "Final Recommendation generated successfully."
    )

    return state