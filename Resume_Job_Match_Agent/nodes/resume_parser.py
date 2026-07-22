"""
nodes/resume_parser.py

Production Ready Resume Parser Agent
"""

from __future__ import annotations

import json
import re
from collections import OrderedDict

from config import llm
from logger import LOGGER
from prompts import RESUME_PARSER_PROMPT
from state import JobMatchState
from tools.skill_normalizer import normalize_skill_list


# ==========================================================
# KNOWN SKILLS
# ==========================================================

KNOWN_SKILLS = {

    # Programming
    "python",
    "java",
    "sql",
    "mysql",
    "sqlite",

    # Data
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "keras",

    # AI/ML
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "generative ai",

    # GenAI
    "langchain",
    "langgraph",
    "rag",
    "retrieval augmented generation",
    "embeddings",
    "vector database",
    "prompt engineering",
    "agentic ai",
    "gemini",
    "gemini api",

    # SAP
    "sap btp",
    "sap hana",
    "sap hana cloud",
    "sap ai core",
    "sap generative ai hub",
    "sap joule",
    "cap",
    "integration suite",

    # Backend
    "fastapi",
    "rest api",
    "api",

    # Cloud
    "cloud computing",
    "docker",
    "kubernetes",
    "linux",

    # Tools
    "git",
    "github",

    # Projects
    "yolo",
    "yolov8",
    "yolov11",
    "opencv",
    "streamlit",
    "playwright",
}
# ==========================================================
# PROJECT BASED ENRICHMENT
# ==========================================================

PROJECT_SKILL_MAP = {

    "yolo": [
        "computer vision",
        "deep learning",
        "opencv",
    ],

    "langchain": [
        "prompt engineering",
        "llm",
        "embeddings",
    ],

    "langgraph": [
        "agentic ai",
        "rag",
    ],

    "streamlit": [
        "python",
        "data visualization",
    ],

    "playwright": [
        "automation testing",
        "typescript",
    ],

    "sap hana": [
        "sql",
        "database",
    ],

    "sap btp": [
        "cloud computing",
    ],
}


# ==========================================================
# CERTIFICATION ENRICHMENT
# ==========================================================

CERTIFICATION_MAP = {

    "aws": [
        "cloud computing",
        "aws",
    ],

    "azure": [
        "cloud computing",
        "azure",
    ],

    "google": [
        "cloud computing",
    ],

    "sap": [
        "sap btp",
    ],
}
# ==========================================================
# JSON EXTRACTION
# ==========================================================

def _extract_json(text) -> dict:
    """
    Extract JSON returned by the LLM.

    Supports:
    - Plain JSON
    - ```json fenced blocks
    - List responses
    - Mixed content
    """

    if isinstance(text, list):

        parts = []

        for item in text:

            if isinstance(item, dict):
                parts.append(item.get("text", ""))

            elif hasattr(item, "text"):
                parts.append(item.text)

            else:
                parts.append(str(item))

        text = "\n".join(parts)

    if not isinstance(text, str):
        text = str(text)

    text = text.strip()

    text = re.sub(
        r"^```json",
        "",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"^```",
        "",
        text,
    )

    text = re.sub(
        r"```$",
        "",
        text,
    ).strip()

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        return {}

    try:
        return json.loads(
            text[start:end + 1]
        )

    except Exception:

        LOGGER.warning(
            "Unable to parse LLM JSON response."
        )

        return {}


# ==========================================================
# KEYWORD EXTRACTION
# ==========================================================

def _extract_known_skills(
    resume_text: str,
) -> list[str]:
    """
    Extract skills using regex word matching.

    Uses word boundaries to avoid:

        java -> javascript
        cap -> capability
    """

    text = resume_text.lower()

    extracted = []

    for skill in KNOWN_SKILLS:

        pattern = rf"\b{re.escape(skill)}\b"

        if re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        ):
            extracted.append(skill)

    return extracted


# ==========================================================
# PROJECT ENRICHMENT
# ==========================================================

def _infer_project_skills(
    resume_text: str,
) -> list[str]:
    """
    Infer additional skills from projects.
    """

    text = resume_text.lower()

    inferred = []

    for keyword, skills in PROJECT_SKILL_MAP.items():

        pattern = rf"\b{re.escape(keyword)}\b"

        if re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        ):
            inferred.extend(skills)

    return inferred


# ==========================================================
# CERTIFICATION ENRICHMENT
# ==========================================================

def _infer_certification_skills(
    certifications: list[str],
) -> list[str]:
    """
    Infer skills from certifications.
    """

    inferred = []

    for certificate in certifications:

        value = certificate.lower()

        for keyword, skills in CERTIFICATION_MAP.items():

            if keyword in value:
                inferred.extend(skills)

    return inferred


# ==========================================================
# EXPERIENCE ENRICHMENT
# ==========================================================

def _infer_experience_skills(
    experience: str,
) -> list[str]:
    """
    Infer generic professional skills
    from experience.
    """

    if not experience:
        return []

    text = experience.lower()

    inferred = []

    if "intern" in text:

        inferred.extend(
            [
                "industry experience",
                "team collaboration",
            ]
        )

    if "developer" in text:

        inferred.append(
            "software development"
        )

    if "engineer" in text:

        inferred.append(
            "engineering"
        )

    return inferred


# ==========================================================
# ORDER PRESERVING DEDUPLICATION
# ==========================================================

def _remove_duplicates(
    skills: list[str],
) -> list[str]:
    """
    Remove duplicates while
    preserving original order.
    """

    return list(
        OrderedDict.fromkeys(
            skills
        )
    )
# ==========================================================
# RESUME PARSER NODE
# ==========================================================

def resume_parser_node(
    state: JobMatchState,
) -> JobMatchState:
    """
    Resume Parser Agent

    Workflow
    --------
    Resume
        ↓
    LLM Extraction
        ↓
    Keyword Extraction
        ↓
    Project Skill Inference
        ↓
    Certification Skill Inference
        ↓
    Experience Skill Inference
        ↓
    Merge
        ↓
    Normalize
        ↓
    Remove Duplicates
        ↓
    Store in State
    """

    LOGGER.info("Running Resume Parser Agent")

    prompt = RESUME_PARSER_PROMPT.invoke(
        {
            "resume": state["resume_text"],
        }
    )

    response = llm.invoke(prompt)

    parsed_resume = _extract_json(
        response.content
    )

    # ------------------------------------------------------
    # Default Values
    # ------------------------------------------------------

    parsed_resume.setdefault(
        "candidate_name",
        "",
    )

    parsed_resume.setdefault(
        "email",
        "",
    )

    parsed_resume.setdefault(
        "phone",
        "",
    )

    parsed_resume.setdefault(
        "total_experience",
        "",
    )

    parsed_resume.setdefault(
        "education",
        [],
    )

    parsed_resume.setdefault(
        "core_skills",
        [],
    )

    parsed_resume.setdefault(
        "projects",
        [],
    )

    parsed_resume.setdefault(
        "certifications",
        [],
    )

    resume_text = state["resume_text"]

    # ------------------------------------------------------
    # LLM Skills
    # ------------------------------------------------------

    llm_skills = parsed_resume.get(
        "core_skills",
        [],
    )

    # ------------------------------------------------------
    # Keyword Extraction
    # ------------------------------------------------------

    keyword_skills = _extract_known_skills(
        resume_text,
    )

    # ------------------------------------------------------
    # Project Enrichment
    # ------------------------------------------------------

    project_skills = _infer_project_skills(
        resume_text,
    )

    # ------------------------------------------------------
    # Certification Enrichment
    # ------------------------------------------------------

    certification_skills = (
        _infer_certification_skills(
            parsed_resume.get(
                "certifications",
                [],
            )
        )
    )

    # ------------------------------------------------------
    # Experience Enrichment
    # ------------------------------------------------------

    experience_skills = (
        _infer_experience_skills(
            parsed_resume.get(
                "total_experience",
                "",
            )
        )
    )

    # ------------------------------------------------------
    # Merge All Skills
    # ------------------------------------------------------

    merged_skills = (
        llm_skills
        + keyword_skills
        + project_skills
        + certification_skills
        + experience_skills
    )

    # ------------------------------------------------------
    # Normalize Skills
    # ------------------------------------------------------

    normalized_skills = normalize_skill_list(
        merged_skills
    )

    # ------------------------------------------------------
    # Remove Duplicates
    # ------------------------------------------------------

    normalized_skills = _remove_duplicates(
        normalized_skills
    )

    # ------------------------------------------------------
    # Sort Alphabetically
    # ------------------------------------------------------

    normalized_skills = sorted(
        normalized_skills,
        key=str.lower,
    )

    parsed_resume["core_skills"] = (
        normalized_skills
    )

    state["parsed_resume"] = parsed_resume

    LOGGER.info(
        "Resume parsed successfully."
    )

    LOGGER.info(
        "Extracted %d skills.",
        len(normalized_skills),
    )

    LOGGER.debug(
        "Skills: %s",
        normalized_skills,
    )

    return state