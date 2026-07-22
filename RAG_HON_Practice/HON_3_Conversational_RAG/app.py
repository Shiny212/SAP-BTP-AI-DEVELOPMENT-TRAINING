"""
app.py

Conversational RAG API with Memory.
"""

from __future__ import annotations


from pathlib import Path


from fastapi import FastAPI


from models.schemas import (
    SessionResponse,
    ChatRequest,
    ChatResponse,
    HistoryResponse,
)


from memory.session_memory import (
    create_session,
    get_history,
    add_message,
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


from rag.query_rewriter import (
    rewrite_question,
)


from rag.retriever import (
    retrieve_similar_chunks,
)


from rag.generator import (
    generate_answer,
)


app = FastAPI(
    title="Conversational RAG API",
    version="1.0",
)


# =====================================================
# Load HR Document
# =====================================================

def load_documents():
    """
    Load HR document into vector store.
    """

    file_path = Path(
        "data/hr_policy.txt"
    )

    text = file_path.read_text(
        encoding="utf-8"
    )


    chunks = split_document(
        text
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
                "hr_policy.txt",
            }
        )


    add_documents(
        documents
    )



# =====================================================
# Health Endpoint
# =====================================================

@app.get("/health")
def health():
    """
    Health check endpoint.
    """

    return {
        "status": "ok"
    }



# =====================================================
# Create New Session
# =====================================================

@app.post(
    "/session/new",
    response_model=SessionResponse,
)
def new_session():
    """
    Create a new conversation session.
    """

    session_id = create_session()


    return {
        "session_id": session_id
    }



# =====================================================
# Chat Endpoint
# =====================================================

@app.post(
    "/chat",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
):
    """
    Chat with conversational memory.
    """


    history = get_history(
        request.session_id
    )


    # Convert follow-up question
    # into standalone question

    standalone_question = rewrite_question(
        request.question,
        history,
    )


    # Retrieve relevant documents

    retrieved_chunks = retrieve_similar_chunks(
        standalone_question,
        top_k=3,
    )


    # Generate grounded answer

    result = generate_answer(
        standalone_question,
        retrieved_chunks,
    )


    # Store conversation history

    add_message(
        request.session_id,
        request.question,
        result["answer"],
    )


    return {
        "session_id":
        request.session_id,

        "answer":
        result["answer"],

        "sources_used":
        result["sources_used"],
    }



# =====================================================
# Get Session History
# =====================================================

@app.get(
    "/session/{session_id}/history",
    response_model=HistoryResponse,
)
def session_history(
    session_id: str,
):
    """
    Return conversation history.
    """

    messages = get_history(
        session_id
    )


    return {
        "session_id":
        session_id,

        "messages":
        messages,
    }



# =====================================================
# Application Startup
# =====================================================

@app.on_event("startup")
def startup_event():
    """
    Load documents when API starts.
    """

    load_documents()