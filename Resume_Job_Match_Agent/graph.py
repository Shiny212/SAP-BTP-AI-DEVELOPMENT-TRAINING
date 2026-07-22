"""
graph.py

LangGraph workflow definition for the
Resume Job Match Agent.
"""

from __future__ import annotations

from langgraph.graph import END
from langgraph.graph import START
from langgraph.graph import StateGraph

from nodes.cover_letter import cover_letter_node
from nodes.final_recommendation import (
    final_recommendation_node,
)
from nodes.fit_score import fit_score_node
from nodes.gap_analysis import gap_analysis_node
from nodes.human_review import (
    human_review_node,
)
from nodes.input_validator import (
    input_validator_node,
)
from nodes.jd_parser import jd_parser_node
from nodes.learning_roadmap import (
    learning_roadmap_node,
)
from nodes.resume_bullet_generator import (
    resume_bullet_generator_node,
)
from nodes.resume_improvement import (
    resume_improvement_node,
)
from nodes.resume_parser import (
    resume_parser_node,
)
from nodes.skill_matcher import (
    skill_matching_node,
)
from state import JobMatchState


def route_based_on_fit_score(
    state: JobMatchState,
) -> str:
    """
    Conditional routing based on fit score.

    >= 80  -> Human Review
    60-79  -> Resume Improvement
    < 60   -> Learning Roadmap
    """

    score = state["fit_score"]

    if score >= 80:
        return "human_review"

    if score >= 60:
        return "resume_improvement"

    return "learning_roadmap"


def route_after_human_review(
    state: JobMatchState,
) -> str:
    """
    Route after Human Review.
    """

    review = state.get(
        "human_review",
        {},
    )

    if review.get(
        "approved",
        False,
    ):
        return "cover_letter"

    return "final_recommendation"


workflow = StateGraph(
    JobMatchState
)

# ==========================================================
# Register Nodes
# ==========================================================

workflow.add_node(
    "input_validator",
    input_validator_node,
)

workflow.add_node(
    "resume_parser",
    resume_parser_node,
)

workflow.add_node(
    "resume_bullet_generator",
    resume_bullet_generator_node,
)

workflow.add_node(
    "jd_parser",
    jd_parser_node,
)

workflow.add_node(
    "skill_matcher",
    skill_matching_node,
)

workflow.add_node(
    "gap_analysis",
    gap_analysis_node,
)

workflow.add_node(
    "fit_score",
    fit_score_node,
)

workflow.add_node(
    "resume_improvement",
    resume_improvement_node,
)

workflow.add_node(
    "learning_roadmap",
    learning_roadmap_node,
)

workflow.add_node(
    "human_review",
    human_review_node,
)

workflow.add_node(
    "cover_letter",
    cover_letter_node,
)

workflow.add_node(
    "final_recommendation",
    final_recommendation_node,
)

# ==========================================================
# Main Workflow
# ==========================================================

workflow.add_edge(
    START,
    "input_validator",
)

workflow.add_edge(
    "input_validator",
    "resume_parser",
)

workflow.add_edge(
    "resume_parser",
    "resume_bullet_generator",
)

workflow.add_edge(
    "resume_bullet_generator",
    "jd_parser",
)

workflow.add_edge(
    "jd_parser",
    "skill_matcher",
)

workflow.add_edge(
    "skill_matcher",
    "gap_analysis",
)

workflow.add_edge(
    "gap_analysis",
    "fit_score",
)
# ==========================================================
# Conditional Routing
# ==========================================================

workflow.add_conditional_edges(
    "fit_score",
    route_based_on_fit_score,
    {
        "human_review": "human_review",
        "resume_improvement": "resume_improvement",
        "learning_roadmap": "learning_roadmap",
    },
)

workflow.add_conditional_edges(
    "human_review",
    route_after_human_review,
    {
        "cover_letter": "cover_letter",
        "final_recommendation": "final_recommendation",
    },
)

# ==========================================================
# Final Paths
# ==========================================================

workflow.add_edge(
    "resume_improvement",
    "final_recommendation",
)

workflow.add_edge(
    "learning_roadmap",
    "final_recommendation",
)

workflow.add_edge(
    "cover_letter",
    "final_recommendation",
)

workflow.add_edge(
    "final_recommendation",
    END,
)

graph = workflow.compile()


def run(
    state: JobMatchState,
) -> JobMatchState:
    """
    Execute the complete workflow.
    """

    return graph.invoke(
        state
    )


if __name__ == "__main__":

    png_data = (
        graph.get_graph()
        .draw_mermaid_png()
    )

    with open(
        "workflow_graph.png",
        "wb",
    ) as file:

        file.write(
            png_data
        )

    print(
        "Workflow graph generated successfully!"
    )