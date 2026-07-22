"""
prompts.py

Prompt templates used by the Resume Job Match Agent.
"""

from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate


# ==========================================================
# Resume Parser Prompt
# ==========================================================

RESUME_PARSER_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert Resume Parser.

Extract only the information present in the resume.

Return ONLY valid JSON.

Required JSON format:

{{
    "candidate_name":"",
    "total_experience":"",
    "core_skills":[],
    "projects":[],
    "certifications":[]
}}
""",
        ),
        (
            "human",
            """
Resume

{resume}
""",
        ),
    ]
)


# ==========================================================
# Job Description Parser Prompt
# ==========================================================

JD_PARSER_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert Job Description Parser.

Extract important hiring requirements.

Return ONLY valid JSON.

Format:

{{
    "job_title":"",
    "required_skills":[],
    "preferred_skills":[],
    "experience_required":""
}}
""",
        ),
        (
            "human",
            """
Job Description

{job_description}
""",
        ),
    ]
)


# ==========================================================
# Skill Matching Prompt
# ==========================================================

SKILL_MATCHING_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an SAP Technical Recruiter.

Compare the candidate skills with the job description.

Return ONLY JSON.

{{
    "matched_skills":[],
    "partially_matched_skills":[],
    "missing_skills":[]
}}
""",
        ),
        (
            "human",
            """
Candidate Skills

{resume_skills}

Required Skills

{required_skills}

Preferred Skills

{preferred_skills}
""",
        ),
    ]
)


# ==========================================================
# Gap Analysis Prompt
# ==========================================================

GAP_ANALYSIS_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an SAP Career Coach.

Explain

• strengths

• missing skills

• weak areas

• improvements

Return only plain text.
""",
        ),
        (
            "human",
            """
Matched Skills

{matched}

Missing Skills

{missing}
""",
        ),
    ]
)


# ==========================================================
# Resume Improvement Prompt
# ==========================================================

RESUME_IMPROVEMENT_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a professional resume writer.

Provide resume improvement suggestions.

Focus on

• SAP BTP

• SAP AI Core

• Joule

• Integration Suite

• CAP

• HANA Cloud

• LangGraph

• RAG

• Agentic AI

Return plain text.
""",
        ),
        (
            "human",
            """
Resume

{resume}

Missing Skills

{missing}
""",
        ),
    ]
)


# ==========================================================
# Cover Letter Prompt
# ==========================================================

COVER_LETTER_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
Write a professional cover letter.

Length:

250-350 words.

Mention

SAP BTP

Generative AI

AI Core

LangGraph

RAG

CAP

HANA Cloud

Prompt Engineering

Enterprise AI

Return only the cover letter.
""",
        ),
        (
            "human",
            """
Resume

{resume}

Job Description

{job_description}
""",
        ),
    ]
)


# ==========================================================
# Recruiter Message Prompt
# ==========================================================

RECRUITER_MESSAGE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
Write a LinkedIn recruiter message.

Length:

120 words maximum.

Professional.

Friendly.

Return only the message.
""",
        ),
        (
            "human",
            """
Resume

{resume}

Job Description

{job_description}
""",
        ),
    ]
)


# ==========================================================
# Learning Roadmap Prompt
# ==========================================================

LEARNING_ROADMAP_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
Create a learning roadmap.

For every missing skill provide

Skill

Reason

Learning Order

Mini Project

Expected Outcome

Return plain text.
""",
        ),
        (
            "human",
            """
Missing Skills

{missing}
""",
        ),
    ]
)


# ==========================================================
# Final Recommendation Prompt
# ==========================================================

FINAL_RECOMMENDATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
Generate the final career recommendation.

Include

Fit Score

Fit Level

Matched Skills

Missing Skills

Gap Analysis

Resume Improvements

Should Apply?

Reason

Return professional report.
""",
        ),
        (
            "human",
            """
Fit Score

{fit_score}

Fit Level

{fit_level}

Matched Skills

{matched}

Missing Skills

{missing}

Gap Analysis

{gap_analysis}

Resume Suggestions

{resume_suggestions}

Learning Roadmap

{learning_plan}
""",
        ),
    ]
)
# ==========================================================
# Resume Bullet Generator Prompt
# ==========================================================

RESUME_BULLET_GENERATOR_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert ATS Resume Writer and Career Coach.

Rewrite the candidate's experience into ATS-friendly
resume bullet points.

Rules

1. Use strong action verbs.
2. Make every bullet achievement-oriented.
3. Include relevant SAP keywords.
4. Align bullets with the target job description.
5. Do not invent experience.
6. Return only bullet points.
7. Generate 6-10 bullet points.
""",
        ),
        (
            "human",
            """
Candidate Resume

{resume}


Target Job Description

{job_description}


Generate ATS-optimized resume bullet points.
""",
        ),
    ]
)