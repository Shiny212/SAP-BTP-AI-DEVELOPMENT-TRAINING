"""
nodes/jd_parser.py

Job Description Parser Agent
"""

from __future__ import annotations

import json
import re

from config import llm
from logger import LOGGER
from prompts import JD_PARSER_PROMPT
from state import JobMatchState
from tools.skill_normalizer import normalize_skill_list


def _extract_json(text) -> dict:
    """
    Extract JSON object from the LLM response.
    Supports both string and list-based responses.
    """

    # Convert list responses into a single string
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

    # Convert any other type to string
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
        return json.loads(text[start:end + 1])

    except Exception:
        return {}


def jd_parser_node(
    state: JobMatchState,
) -> JobMatchState:
    """
    Job Description Parser Agent.
    """

    LOGGER.info("Running Job Description Parser Agent")

    prompt = JD_PARSER_PROMPT.invoke(
        {
            "job_description": state["job_description"],
        }
    )

    response = llm.invoke(prompt)

    parsed_jd = _extract_json(
        response.content
    )

    parsed_jd.setdefault(
        "job_title",
        "",
    )

    parsed_jd.setdefault(
        "required_skills",
        [],
    )

    parsed_jd.setdefault(
        "preferred_skills",
        [],
    )

    parsed_jd.setdefault(
        "experience_required",
        "",
    )

    parsed_jd["required_skills"] = normalize_skill_list(
        parsed_jd["required_skills"]
    )

    parsed_jd["preferred_skills"] = normalize_skill_list(
        parsed_jd["preferred_skills"]
    )

    state["parsed_jd"] = parsed_jd
    LOGGER.info(
        "Required Skills: %s",
        parsed_jd["required_skills"],
    )

    LOGGER.info(
        "Preferred Skills: %s",
        parsed_jd["preferred_skills"],
    )

    LOGGER.info(
        "Job Description parsed successfully."
    )

    return state