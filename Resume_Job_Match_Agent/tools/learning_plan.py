"""
tools/learning_plan.py

Learning Roadmap Generator
"""

from __future__ import annotations

from typing import Dict
from typing import List


LEARNING_RESOURCES: Dict[str, Dict[str, str]] = {
    "SAP Joule": {
        "reason": "Enterprise AI copilot for SAP applications.",
        "priority": "High",
        "duration": "1 Week",
        "project": "Build a Joule-powered SAP assistant.",
    },
    "SAP AI Core": {
        "reason": "Deploy and manage AI models on SAP BTP.",
        "priority": "High",
        "duration": "2 Weeks",
        "project": "Deploy an ML model using SAP AI Core.",
    },
    "SAP Generative AI Hub": {
        "reason": "Develop enterprise GenAI applications on SAP.",
        "priority": "High",
        "duration": "2 Weeks",
        "project": "Create an AI chatbot using GenAI Hub.",
    },
    "SAP CAP": {
        "reason": "Develop cloud-native SAP applications.",
        "priority": "High",
        "duration": "2 Weeks",
        "project": "Build a CAP CRUD application.",
    },
    "SAP Integration Suite": {
        "reason": "Integrate enterprise SAP and non-SAP systems.",
        "priority": "High",
        "duration": "2 Weeks",
        "project": "Create an integration flow using Cloud Integration.",
    },
    "SAP HANA Cloud": {
        "reason": "Enterprise cloud database platform.",
        "priority": "Medium",
        "duration": "2 Weeks",
        "project": "Create HANA Cloud tables and SQL views.",
    },
    "SAP Build Apps": {
        "reason": "Low-code application development.",
        "priority": "Medium",
        "duration": "1 Week",
        "project": "Develop a no-code employee application.",
    },
    "SAP Build Process Automation": {
        "reason": "Workflow and process automation.",
        "priority": "Medium",
        "duration": "1 Week",
        "project": "Automate an approval workflow.",
    },
    "SAP Workflow Management": {
        "reason": "Business workflow orchestration.",
        "priority": "Medium",
        "duration": "1 Week",
        "project": "Implement leave approval workflow.",
    },
    "LangChain": {
        "reason": "LLM application framework.",
        "priority": "High",
        "duration": "1 Week",
        "project": "Build a Retrieval-Augmented Generation chatbot.",
    },
    "LangGraph": {
        "reason": "Agentic AI workflow orchestration.",
        "priority": "High",
        "duration": "2 Weeks",
        "project": "Develop a multi-agent LangGraph workflow.",
    },
    "RAG": {
        "reason": "Enterprise knowledge retrieval.",
        "priority": "High",
        "duration": "1 Week",
        "project": "Implement a document Q&A system.",
    },
    "GraphRAG": {
        "reason": "Knowledge graph enhanced retrieval.",
        "priority": "Medium",
        "duration": "2 Weeks",
        "project": "Create a GraphRAG-based assistant.",
    },
    "Vector Database": {
        "reason": "Store and search embeddings.",
        "priority": "Medium",
        "duration": "1 Week",
        "project": "Integrate ChromaDB with LangChain.",
    },
    "Prompt Engineering": {
        "reason": "Improve LLM response quality.",
        "priority": "High",
        "duration": "3 Days",
        "project": "Create optimized prompts for enterprise AI.",
    },
    "Agentic AI": {
        "reason": "Design autonomous AI workflows.",
        "priority": "High",
        "duration": "2 Weeks",
        "project": "Build a multi-agent enterprise assistant.",
    },
}


def generate_learning_plan(
    missing_skills: List[str],
) -> str:
    """
    Generate a structured learning roadmap.
    """

    if not missing_skills:
        return (
            "No learning roadmap required.\n"
            "The candidate already satisfies the required skills."
        )

    roadmap: List[str] = []

    roadmap.append("=" * 70)
    roadmap.append("PERSONALIZED LEARNING ROADMAP")
    roadmap.append("=" * 70)
    roadmap.append("")

    for index, skill in enumerate(missing_skills, start=1):

        resource = LEARNING_RESOURCES.get(
            skill,
            {
                "reason": "Improve practical knowledge.",
                "priority": "Medium",
                "duration": "1 Week",
                "project": "Complete a hands-on project.",
            },
        )

        roadmap.append(f"{index}. {skill}")
        roadmap.append(f"Priority      : {resource['priority']}")
        roadmap.append(f"Reason        : {resource['reason']}")
        roadmap.append(f"Duration      : {resource['duration']}")
        roadmap.append(f"Mini Project  : {resource['project']}")
        roadmap.append("")

    roadmap.append("=" * 70)
    roadmap.append("Suggested Learning Order")
    roadmap.append("=" * 70)
    roadmap.append("")

    high = []
    medium = []
    low = []

    for skill in missing_skills:

        priority = LEARNING_RESOURCES.get(
            skill,
            {"priority": "Medium"},
        )["priority"]

        if priority == "High":
            high.append(skill)

        elif priority == "Medium":
            medium.append(skill)

        else:
            low.append(skill)

    if high:
        roadmap.append("High Priority")
        for skill in high:
            roadmap.append(f"• {skill}")
        roadmap.append("")

    if medium:
        roadmap.append("Medium Priority")
        for skill in medium:
            roadmap.append(f"• {skill}")
        roadmap.append("")

    if low:
        roadmap.append("Low Priority")
        for skill in low:
            roadmap.append(f"• {skill}")
        roadmap.append("")

    roadmap.append("=" * 70)
    roadmap.append("Expected Outcome")
    roadmap.append("=" * 70)
    roadmap.append(
        "After completing this roadmap, the candidate should be able to "
        "confidently apply for SAP BTP + Generative AI roles."
    )

    return "\n".join(roadmap)