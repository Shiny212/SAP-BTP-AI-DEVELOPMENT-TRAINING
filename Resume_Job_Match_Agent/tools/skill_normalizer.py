"""
tools/skill_normalizer.py

Normalize skills using SAP Skill Taxonomy
and built-in aliases.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

TAXONOMY_FILE = Path(
    "data/sap_skill_taxonomy.json"
)

# ----------------------------------------------------------
# Built-in aliases
# ----------------------------------------------------------

DEFAULT_ALIASES = {
    "python": [
        "python3",
        "python programming",
    ],

    "git": [
        "github",
        "gitlab",
        "bitbucket",
    ],

    "machine learning": [
        "ml",
    ],

    "artificial intelligence": [
        "ai",
    ],

    "generative ai": [
        "gen ai",
        "genai",
    ],

    "langchain": [
        "lang chain",
    ],

    "langgraph": [
        "lang graph",
    ],

    "retrieval augmented generation": [
        "rag",
    ],

    "sap btp": [
        "business technology platform",
        "sap business technology platform",
    ],

    "sap hana cloud": [
        "hana",
        "sap hana",
    ],

    "sap ai core": [
        "ai core",
    ],

    "cloud application programming model": [
        "cap",
    ],

    "integration suite": [
        "sap integration suite",
    ],

    "vector database": [
        "vector db",
        "vectordb",
    ],

    "embeddings": [
        "embedding",
    ],

    "rest api": [
        "rest",
        "restful api",
    ],

    "fastapi": [
        "fast api",
    ],

    "tensorflow": [
        "tensor flow",
    ],

    "scikit-learn": [
        "sklearn",
        "scikit learn",
    ],

    "playwright": [
        "play wright",
    ],

    "docker": [
        "docker container",
    ],

    "kubernetes": [
        "k8s",
    ],

    "sql": [
        "mysql",
        "sqlite",
        "postgres",
        "postgresql",
    ],

    "yolo": [
        "yolov8",
        "yolov11",
    ],
}


# ----------------------------------------------------------
# Load taxonomy
# ----------------------------------------------------------

def load_taxonomy() -> dict:
    """
    Load SAP taxonomy JSON.
    """

    if not TAXONOMY_FILE.exists():
        return DEFAULT_ALIASES.copy()

    with open(
        TAXONOMY_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        taxonomy = json.load(file)

    merged = DEFAULT_ALIASES.copy()

    for canonical, aliases in taxonomy.items():

        merged.setdefault(
            canonical,
            [],
        )

        merged[canonical].extend(aliases)

    return merged


TAXONOMY = load_taxonomy()


# ----------------------------------------------------------
# Normalize one skill
# ----------------------------------------------------------

def normalize_skill(
    skill: str,
) -> str:
    """
    Normalize a single skill.
    """

    if not skill:
        return ""

    skill = skill.lower().strip()

    skill = re.sub(
        r"\s+",
        " ",
        skill,
    )

    for canonical, aliases in TAXONOMY.items():

        if skill == canonical.lower():
            return canonical.title()

        for alias in aliases:

            if skill == alias.lower():
                return canonical.title()

    return skill.title()


# ----------------------------------------------------------
# Normalize list
# ----------------------------------------------------------

def normalize_skill_list(
    skills: list[str],
) -> list[str]:
    """
    Normalize skill list.
    """

    normalized = []

    seen = set()

    for skill in skills:

        normalized_skill = normalize_skill(
            skill
        )

        key = normalized_skill.lower()

        if key not in seen:

            normalized.append(
                normalized_skill
            )

            seen.add(key)

    return normalized