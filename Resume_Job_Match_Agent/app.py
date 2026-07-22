"""
app.py

Entry point for the Resume Job Match Agent.
Supports TXT and PDF resumes.
"""

from __future__ import annotations

from pathlib import Path

from graph import run
from logger import LOGGER
from state import JobMatchState
from tools.memory import get_previous_jobs
from tools.pdf_loader import extract_text


def load_document(file_path: str) -> str:
    """
    Load a TXT or PDF document.

    Parameters
    ----------
    file_path : str
        Path to the document.

    Returns
    -------
    str
        Extracted text.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    extension = path.suffix.lower()

    if extension == ".txt":
        return path.read_text(
            encoding="utf-8"
        )

    if extension == ".pdf":
        return extract_text(
            str(path)
        )

    raise ValueError(
        f"Unsupported file type: {extension}"
    )


def main() -> None:
    """
    Run the Resume Job Match Agent.
    """

    LOGGER.info(
        "Starting Resume Job Match Agent"
    )

    resume_path = input(
        "Enter Resume file (.txt/.pdf): "
    ).strip()

    jd_path = input(
        "Enter Job Description (.txt): "
    ).strip()

    resume_text = load_document(
        resume_path
    )

    job_description = load_document(
        jd_path
    )

    previous_jobs = get_previous_jobs()

    initial_state: JobMatchState = {

    "resume_text": resume_text,

    "job_description": job_description,


    # Parsed Data

    "parsed_resume": {},

    "parsed_jd": {},


    # Skill Matching

    "matched_skills": [],

    "partially_matched_skills": [],

    "missing_skills": [],


    # Analysis

    "gap_analysis": "",

    "fit_score": 0,

    "fit_level": "",

    "apply_recommendation": "",


    "resume_improvement_suggestions": "",

    "learning_roadmap": "",


    # Resume Enhancement

    "generated_resume_bullets": "",


    # Cover Letter

    "cover_letter": "",

    "recruiter_message": "",


    # Human-in-the-Loop

    "human_review": None,

    "workflow_status": None,


    # Memory

    "previous_job_descriptions": previous_jobs,


    # Final Output

    "final_recommendation": "",
}
    LOGGER.info(
        "Workflow started..."
    )

    final_state = run(
        initial_state
    )

    LOGGER.info(
        "Workflow completed successfully."
    )

    print("\n")
    print("=" * 100)
    print("FINAL RECOMMENDATION")
    print("=" * 100)
    print()

    print(
        final_state[
            "final_recommendation"
        ]
    )

    output_file = Path(
        "final_recommendation_report.txt"
    )

    output_file.write_text(
        final_state[
            "final_recommendation"
        ],
        encoding="utf-8",
    )

    LOGGER.info(
        "Final report saved to %s",
        output_file.resolve(),
    )

    print()
    print(
        f"Report saved to: {output_file.resolve()}"
    )


if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        LOGGER.warning(
            "Application interrupted by user."
        )

        print(
            "\nOperation cancelled by user."
        )

    except FileNotFoundError as error:

        LOGGER.error(
            str(error)
        )

        print(
            f"\nError: {error}"
        )

    except ValueError as error:

        LOGGER.error(
            str(error)
        )

        print(
            f"\nError: {error}"
        )

    except Exception as error:

        LOGGER.exception(
            "Unexpected error occurred."
        )

        print(
            "\nAn unexpected error occurred."
        )

        print(error)