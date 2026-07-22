"""
rag/quality_checker.py

Checks whether generated answer
is supported by retrieved documents.
"""

from __future__ import annotations


def check_answer_quality(
    answer: str,
    retrieved_chunks: list[dict],
) -> dict:
    """
    Verify answer support using retrieved chunks.
    """


    if not retrieved_chunks:

        return {
            "supported_by_documents": False,
            "confidence": "low",
        }


    context = " ".join(
        [
            chunk["text"].lower()
            for chunk in retrieved_chunks
        ]
    )


    answer_words = set(
        answer.lower().split()
    )


    context_words = set(
        context.split()
    )


    common_words = (
        answer_words
        &
        context_words
    )


    if len(answer_words) == 0:

        return {
            "supported_by_documents": False,
            "confidence": "low",
        }


    support_ratio = (
        len(common_words)
        /
        len(answer_words)
    )


    if support_ratio >= 0.7:

        return {
            "supported_by_documents": True,
            "confidence": "high",
        }


    if support_ratio >= 0.4:

        return {
            "supported_by_documents": True,
            "confidence": "medium",
        }


    return {
        "supported_by_documents": False,
        "confidence": "low",
    }