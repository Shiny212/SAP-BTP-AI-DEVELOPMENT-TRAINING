"""
nodes/human_review.py

Human-in-the-Loop Review Agent
"""

from __future__ import annotations

from logger import LOGGER
from state import JobMatchState


def _display_skills(skills: list[str]) -> None:
    """
    Display the extracted skills.
    """

    print("\nCurrent Skills\n")

    if not skills:
        print("No skills found.\n")
        return

    for index, skill in enumerate(skills, start=1):
        print(f"{index}. {skill}")

    print()


def human_review_node(
    state: JobMatchState,
) -> JobMatchState:
    """
    Human reviews AI extracted skills before
    continuing the workflow.

    Available actions:
    - Approve
    - Add Skills
    - Remove Skills
    - View Updated Skills
    - Reject Workflow
    """

    LOGGER.info(
        "Running Human Review Agent"
    )

    resume = state["parsed_resume"]

    skills = list(
        resume.get(
            "core_skills",
            [],
        )
    )

    added_skills = []
    removed_skills = []

    print("\n" + "=" * 70)
    print("        HUMAN-IN-THE-LOOP REVIEW")
    print("=" * 70)

    while True:

        _display_skills(skills)

        print("Options")
        print("1. Approve Skills")
        print("2. Add Skill")
        print("3. Remove Skill")
        print("4. View Skills")
        print("5. Reject Workflow")

        choice = input(
            "\nChoose (1-5): "
        ).strip()

        # --------------------------------------------------
        # APPROVE
        # --------------------------------------------------

        if choice == "1":

            LOGGER.info(
                "Human approved extracted skills."
            )

            state["human_review"] = {
                "approved": True,
                "added_skills": added_skills,
                "removed_skills": removed_skills,
            }

            state["workflow_status"] = "Approved"

            break

        # --------------------------------------------------
        # ADD SKILL
        # --------------------------------------------------

        elif choice == "2":

            new_skill = input(
                "\nEnter skill to add: "
            ).strip()

            if not new_skill:

                print(
                    "\nSkill cannot be empty."
                )

                continue

            exists = any(
                skill.lower() == new_skill.lower()
                for skill in skills
            )

            if exists:

                print(
                    "\nSkill already exists."
                )

                continue

            skills.append(new_skill)

            added_skills.append(new_skill)

            LOGGER.info(
                "Added skill: %s",
                new_skill,
            )

            print(
                f"\n'{new_skill}' added successfully."
            )

        # --------------------------------------------------
        # REMOVE SKILL
        # --------------------------------------------------

        elif choice == "3":

            remove_skill = input(
                "\nEnter skill to remove: "
            ).strip()

            found = False

            updated = []

            for skill in skills:

                if (
                    skill.lower()
                    ==
                    remove_skill.lower()
                ):

                    found = True
                    removed_skills.append(skill)

                else:

                    updated.append(skill)

            if found:

                skills = updated

                LOGGER.info(
                    "Removed skill: %s",
                    remove_skill,
                )

                print(
                    f"\n'{remove_skill}' removed successfully."
                )

            else:

                print(
                    "\nSkill not found."
                )

        # --------------------------------------------------
        # VIEW SKILLS
        # --------------------------------------------------

        elif choice == "4":

            continue

        # --------------------------------------------------
        # REJECT
        # --------------------------------------------------

        elif choice == "5":

            LOGGER.warning(
                "Human rejected workflow."
            )

            state["human_review"] = {
                "approved": False,
                "added_skills": added_skills,
                "removed_skills": removed_skills,
            }

            state["workflow_status"] = "Rejected"

            state["parsed_resume"] = resume

            print(
                "\nWorkflow stopped by user."
            )

            return state

        # --------------------------------------------------
        # INVALID OPTION
        # --------------------------------------------------

        else:

            print(
                "\nInvalid option. Please try again."
            )

    # ------------------------------------------------------
    # Save Updated Skills
    # ------------------------------------------------------

    skills = sorted(
        set(skills),
        key=str.lower,
    )

    resume["core_skills"] = skills

    state["parsed_resume"] = resume

    print("\n" + "=" * 70)
    print("Human Review Summary")
    print("=" * 70)

    print(
        f"Approved : {state['human_review']['approved']}"
    )

    print(
        f"Added Skills : {added_skills if added_skills else 'None'}"
    )

    print(
        f"Removed Skills : {removed_skills if removed_skills else 'None'}"
    )

    print(
        f"Final Skill Count : {len(skills)}"
    )

    LOGGER.info(
        "Human Review Completed Successfully."
    )

    return state