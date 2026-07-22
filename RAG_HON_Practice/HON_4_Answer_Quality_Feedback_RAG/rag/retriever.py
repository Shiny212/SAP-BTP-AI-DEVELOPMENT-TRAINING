"""
rag/retriever.py

Similarity retrieval.
"""

from __future__ import annotations


from sklearn.metrics.pairwise import (
    cosine_similarity,
)


from rag.embeddings import (
    create_query_embedding,
)


from rag.vector_store import (
    get_documents,
)



def retrieve_similar_chunks(
    question: str,
    top_k: int = 3,
) -> list[dict]:
    """
    Retrieve top relevant chunks.
    """

    documents = get_documents()


    if not documents:

        return []


    question_embedding = (
        create_query_embedding(
            question
        )
    )


    scored_documents = []


    for document in documents:

        score = cosine_similarity(
            [
                question_embedding
            ],
            [
                document["embedding"]
            ],
        )[0][0]


        scored_documents.append(
            {
                "text":
                document["text"],

                "source":
                document["source"],

                "score":
                float(score),
            }
        )


    scored_documents.sort(
        key=lambda item: item["score"],
        reverse=True,
    )


    return scored_documents[:top_k]