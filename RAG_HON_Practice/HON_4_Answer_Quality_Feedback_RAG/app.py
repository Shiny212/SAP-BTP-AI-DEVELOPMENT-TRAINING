"""
app.py

Q&A API with Answer Quality Check and Feedback.
"""

from __future__ import annotations


from pathlib import Path


from fastapi import FastAPI


from models.schemas import (
    IngestRequest,
    IngestResponse,
    AskRequest,
    AskResponse,
    FeedbackRequest,
    FeedbackSummaryResponse,
)


from rag.chunker import (
    split_document,
)


from rag.embeddings import (
    create_embeddings,
)


from rag.vector_store import (
    add_documents,
)


from rag.retriever import (
    retrieve_similar_chunks,
)


from rag.generator import (
    generate_answer,
)


from rag.quality_checker import (
    check_answer_quality,
)


from feedback.feedback_store import (
    add_feedback,
    get_feedback_summary,
)



app = FastAPI(
    title="RAG Quality Check API",
    version="1.0",
)



# =====================================================
# Health
# =====================================================

@app.get("/health")
def health():

    return {
        "status": "ok"
    }



# =====================================================
# Ingest
# =====================================================

@app.post(
    "/ingest",
    response_model=IngestResponse,
)
def ingest(
    request: IngestRequest,
):

    chunks = split_document(
        request.text
    )


    embeddings = create_embeddings(
        chunks
    )


    documents = []


    for index, chunk in enumerate(chunks):

        documents.append(
            {
                "text": chunk,

                "embedding":
                embeddings[index],

                "source":
                request.source_name,
            }
        )


    add_documents(
        documents
    )


    return {
        "message":
        "Document ingested successfully",

        "chunks_created":
        len(documents),
    }



# =====================================================
# Ask
# =====================================================

@app.post(
    "/ask",
    response_model=AskResponse,
)
def ask(
    request: AskRequest,
):

    retrieved_chunks = retrieve_similar_chunks(
        request.question,
        top_k=3,
    )


    result = generate_answer(
        request.question,
        retrieved_chunks,
    )


    quality = check_answer_quality(
        result["answer"],
        retrieved_chunks,
    )


    answer = result["answer"]


    if not quality["supported_by_documents"]:

        answer = (
            "Information may not be available "
            "in documents."
        )


    return {
        "answer":
        answer,

        "supported_by_documents":
        quality["supported_by_documents"],

        "confidence":
        quality["confidence"],

        "sources_used":
        result["sources_used"],
    }



# =====================================================
# Feedback
# =====================================================

@app.post("/feedback")
def feedback(
    request: FeedbackRequest,
):

    add_feedback(
        request.question,
        request.helpful,
    )


    return {
        "message":
        "Feedback stored successfully"
    }



# =====================================================
# Feedback Summary
# =====================================================

@app.get(
    "/feedback/summary",
    response_model=FeedbackSummaryResponse,
)
def feedback_summary():

    return get_feedback_summary()