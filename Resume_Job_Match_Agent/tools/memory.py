"""
tools/memory.py

Persistent memory for previous job analyses.
"""

from __future__ import annotations

import json
from pathlib import Path

MEMORY_FILE = Path("memory/history.json")


def load_memory() -> list[dict]:
    """
    Load previous analyses.
    """

    if not MEMORY_FILE.exists():
        return []

    with open(
        MEMORY_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)


def save_memory(
    job_title: str,
    fit_score: int,
    recommendation: str,
) -> None:
    """
    Save one completed analysis.
    """

    history = load_memory()

    history.append(
        {
            "job_title": job_title,
            "fit_score": fit_score,
            "recommendation": recommendation,
        }
    )

    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            history,
            file,
            indent=4,
        )


def get_previous_jobs() -> list[dict]:
    """
    Return all previous analyses.
    """

    return load_memory()