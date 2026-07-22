"""
rag/retriever.py

Similarity search implementation.
"""

from __future__ import annotations

from sklearn.metrics.pairwise import cosine_similarity

from rag.embeddings import create_embedding
from rag.vector_store import get_all_documents


def retrieve_similar_chunks(
    question: str,
    top_k: int = 3,
) -> list[dict]:
    """
    Retrieve top-k similar chunks.
    """

    documents = get_all_documents()

    if not documents:
        return []


    # Create question embedding
    question_vector = create_embedding(
        question
    )


    scored_documents = []


    for document in documents:

        similarity = cosine_similarity(
            [
                question_vector
            ],
            [
                document["embedding"]
            ],
        )[0][0]


        scored_documents.append(
            {
                "text": document["text"],
                "source": document["source"],
                "score": float(similarity),
            }
        )


    scored_documents.sort(
        key=lambda x: x["score"],
        reverse=True,
    )


    return scored_documents[:top_k]