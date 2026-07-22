"""
nodes/resume_improvement.py

Resume Improvement Agent
"""

from __future__ import annotations

from config import llm
from logger import LOGGER
from prompts import RESUME_IMPROVEMENT_PROMPT
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


def resume_improvement_node(
    state: JobMatchState,
) -> JobMatchState:
    """
    Generate resume improvement suggestions.
    """

    LOGGER.info(
        "Running Resume Improvement Agent"
    )

    resume_text = state.get(
        "resume_text",
        "",
    )

    missing_skills = state.get(
        "missing_skills",
        [],
    )

    parsed_resume = state.get(
        "parsed_resume",
        {},
    )

    candidate_name = parsed_resume.get(
        "candidate_name",
        "Candidate",
    )

    prompt = RESUME_IMPROVEMENT_PROMPT.invoke(
        {
            "resume": resume_text,
            "missing": "\n".join(missing_skills),
        }
    )

    response = llm.invoke(prompt)

    suggestions = _get_response_text(
        response
    )

    if missing_skills:

        suggestions += "\n\n"

        suggestions += "=" * 70 + "\n"
        suggestions += "MISSING SKILLS TO INCLUDE\n"
        suggestions += "=" * 70 + "\n"

        for skill in missing_skills:
            suggestions += f"• {skill}\n"

    suggestions += "\n"

    suggestions += "=" * 70 + "\n"
    suggestions += "RECOMMENDED RESUME SECTIONS\n"
    suggestions += "=" * 70 + "\n"

    sections = [
        "Professional Summary",
        "Core Technical Skills",
        "SAP BTP Skills",
        "Generative AI Skills",
        "Agentic AI Projects",
        "Professional Projects",
        "Certifications",
        "Achievements",
    ]

    for section in sections:
        suggestions += f"• {section}\n"

    suggestions += "\n"

    suggestions += "=" * 70 + "\n"
    suggestions += "KEYWORDS TO IMPROVE ATS SCORE\n"
    suggestions += "=" * 70 + "\n"

    ats_keywords = [
        "SAP BTP",
        "SAP AI Core",
        "SAP Generative AI Hub",
        "SAP Joule",
        "SAP CAP",
        "SAP Integration Suite",
        "SAP HANA Cloud",
        "LangGraph",
        "LangChain",
        "Prompt Engineering",
        "RAG",
        "GraphRAG",
        "Vector Database",
        "Enterprise AI",
        "Agentic AI",
    ]

    for keyword in ats_keywords:
        suggestions += f"• {keyword}\n"

    suggestions += "\n"

    suggestions += "=" * 70 + "\n"
    suggestions += "FINAL ADVICE\n"
    suggestions += "=" * 70 + "\n"

    suggestions += (
        f"Update {candidate_name}'s resume by emphasizing "
        "SAP BTP projects, AI Core implementations, "
        "Generative AI Hub experience, LangGraph workflows, "
        "enterprise AI architecture, and measurable project "
        "outcomes. Include quantified achievements wherever "
        "possible to improve recruiter visibility."
    )

    state[
        "resume_improvement_suggestions"
    ] = suggestions

    LOGGER.info(
        "Resume Improvement Agent completed successfully."
    )

    return state