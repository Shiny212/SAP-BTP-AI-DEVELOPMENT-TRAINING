"""
app.py

FastAPI application for Document Q&A RAG API.
"""

from __future__ import annotations


from fastapi import FastAPI
from fastapi.responses import JSONResponse


from models.schemas import (
    IngestRequest,
    IngestResponse,
    QuestionRequest,
    AnswerResponse,
)


from rag.chunker import split_document

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

from utils.logger import LOGGER


# ======================================================
# FastAPI Application
# ======================================================

app = FastAPI(
    title="Document Q&A RAG API",
    description=
    "RAG based Question Answering using Gemini",
    version="1.0",
)


# ======================================================
# Health Check
# ======================================================

@app.get(
    "/health"
)
def health_check():
    """
    Health endpoint.
    """

    return {
        "status": "ok"
    }


# ======================================================
# Ingest Documents
# ======================================================

@app.post(
    "/ingest",
    response_model=IngestResponse,
)
def ingest_documents(
    request: IngestRequest,
):
    """
    Ingest documents into RAG system.

    Steps:
    1. Split documents
    2. Create embeddings
    3. Store in memory
    """

    LOGGER.info(
        "Document ingestion started"
    )


    all_chunks = []


    for document in request.documents:

        chunks = split_document(
            document.text
        )


        for chunk in chunks:

            all_chunks.append(
                {
                    "text": chunk,
                    "source": document.source,
                }
            )


    texts = [
        item["text"]
        for item in all_chunks
    ]


    embeddings = create_embeddings(
        texts
    )


    documents_with_embeddings = []


    for index, item in enumerate(all_chunks):

        documents_with_embeddings.append(
            {
                "text": item["text"],
                "embedding": embeddings[index],
                "source": item["source"],
            }
        )


    add_documents(
        documents_with_embeddings
    )


    LOGGER.info(
        "Created %s chunks",
        len(documents_with_embeddings),
    )


    return IngestResponse(
        message=
        "Documents ingested successfully",
        chunks_created=
        len(documents_with_embeddings),
    )


# ======================================================
# Ask Question
# ======================================================

@app.post(
    "/ask",
    response_model=AnswerResponse,
)
def ask_question(
    request: QuestionRequest,
):
    """
    Answer user question using RAG.
    """

    LOGGER.info(
        "Question received: %s",
        request.question,
    )


    retrieved_chunks = retrieve_similar_chunks(
        request.question,
        top_k=3,
    )


    result = generate_answer(
        question=request.question,
        retrieved_chunks=retrieved_chunks,
    )


    return JSONResponse(
        content=result
    )