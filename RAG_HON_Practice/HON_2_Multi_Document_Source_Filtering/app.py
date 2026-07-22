"""
app.py

Multi Document Q&A API with Source Filtering.
"""

from __future__ import annotations


from fastapi import FastAPI


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


app = FastAPI(
    title="Multi Document Q&A RAG API",
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

    chunks_data = []


    for document in request.documents:

        chunks = split_document(
            document.text
        )


        for chunk in chunks:

            chunks_data.append(
                {
                    "text": chunk,
                    "source_name":
                    document.source_name,

                    "category":
                    document.category,
                }
            )


    texts = [
        item["text"]
        for item in chunks_data
    ]


    embeddings = create_embeddings(
        texts
    )


    final_documents = []


    for index, item in enumerate(chunks_data):

        final_documents.append(
            {
                "text":
                item["text"],

                "embedding":
                embeddings[index],

                "source_name":
                item["source_name"],

                "category":
                item["category"],
            }
        )


    add_documents(
        final_documents
    )


    return {
        "message":
        "Documents ingested successfully",

        "chunks_created":
        len(final_documents),
    }



# =====================================================
# Ask
# =====================================================

@app.post(
    "/ask",
    response_model=AnswerResponse,
)
def ask(
    request: QuestionRequest,
):

    chunks = retrieve_similar_chunks(
        question=request.question,

        category=request.category,

        top_k=3,
    )


    result = generate_answer(
        question=request.question,

        retrieved_chunks=chunks,
    )


    return result