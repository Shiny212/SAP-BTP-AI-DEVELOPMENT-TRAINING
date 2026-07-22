"""
rag/retriever.py

Category filtered similarity search.
"""

from __future__ import annotations


from sklearn.metrics.pairwise import cosine_similarity


from rag.embeddings import (
    create_query_embedding,
)

from rag.vector_store import (
    get_documents_by_category,
)


def retrieve_similar_chunks(
    question: str,
    category: str,
    top_k: int = 3,
) -> list[dict]:
    """
    Retrieve chunks after category filtering.
    """


    documents = get_documents_by_category(
        category
    )


    if not documents:
        return []


    question_vector = create_query_embedding(
        question
    )


    scored_documents = []


    for document in documents:

        score = cosine_similarity(
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
                "source_name": document["source_name"],
                "category": document["category"],
                "score": float(score),
            }
        )


    scored_documents.sort(
        key=lambda item: item["score"],
        reverse=True,
    )


    return scored_documents[:top_k]