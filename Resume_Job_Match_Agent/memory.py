"""
memory.py

Simple memory module for storing and retrieving
previous Job Descriptions.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List

from logger import LOGGER


MEMORY_DIRECTORY = Path("data")

MEMORY_DIRECTORY.mkdir(
    exist_ok=True
)

MEMORY_FILE = (
    MEMORY_DIRECTORY
    / "job_memory.json"
)


def _initialize_memory() -> None:
    """
    Create memory file if it
    does not exist.
    """

    if MEMORY_FILE.exists():
        return

    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump([], file, indent=4)


_initialize_memory()


def load_previous_job_descriptions() -> List[str]:
    """
    Load all previous job descriptions.
    """

    try:

        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

            if isinstance(data, list):
                return data

            return []

    except Exception as error:

        LOGGER.error(error)

        return []


def save_job_description(
    job_description: str,
) -> None:
    """
    Save a job description into memory.
    """

    descriptions = (
        load_previous_job_descriptions()
    )

    cleaned = job_description.strip()

    if cleaned in descriptions:

        LOGGER.info(
            "Job Description already exists in memory."
        )

        return

    descriptions.append(cleaned)

    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            descriptions,
            file,
            indent=4,
            ensure_ascii=False,
        )

    LOGGER.info(
        "Job Description saved to memory."
    )


def compare_with_previous_roles(
    current_job_description: str,
) -> List[str]:
    """
    Compare current JD with
    previously stored JDs.
    """

    previous = (
        load_previous_job_descriptions()
    )

    similar_jobs = []

    current = (
        current_job_description
        .lower()
        .split()
    )

    current_words = set(current)

    for job in previous:

        job_words = set(
            job.lower().split()
        )

        common = (
            current_words
            & job_words
        )

        if len(common) >= 10:

            similar_jobs.append(
                job
            )

    return similar_jobs


def clear_memory() -> None:
    """
    Delete all stored job descriptions.
    """

    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            [],
            file,
            indent=4,
        )

    LOGGER.info(
        "Memory cleared successfully."
    )


def memory_statistics() -> dict:
    """
    Return memory statistics.
    """

    jobs = (
        load_previous_job_descriptions()
    )

    return {
        "total_saved_jobs": len(jobs),
        "memory_file": str(MEMORY_FILE),
    }