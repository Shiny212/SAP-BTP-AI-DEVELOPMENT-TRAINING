"""
rag.py

SmartKart Retrieval-Augmented Generation (RAG)

Features
--------
✓ FAISS Vector Database
✓ HuggingFace Embeddings
✓ LangChain RAG Pipeline
✓ Gemini 3.1 Flash Lite
✓ SmartKart Knowledge Base
"""

from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from config import llm


# ==========================================================
# Constants
# ==========================================================

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 3

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


# ==========================================================
# Load Knowledge Base
# ==========================================================

BASE_DIR = Path(__file__).parent

KNOWLEDGE_FILE = (
    BASE_DIR
    / "knowledge_base"
    / "smartkart_policies.txt"
)

if not KNOWLEDGE_FILE.exists():
    raise FileNotFoundError(
        f"Knowledge base not found:\n{KNOWLEDGE_FILE}"
    )

with open(
    KNOWLEDGE_FILE,
    "r",
    encoding="utf-8"
) as file:

    knowledge_text = file.read()


DOCUMENTS = [
    Document(
        page_content=knowledge_text,
        metadata={
            "source": "SmartKart Knowledge Base"
        },
    )
]


# ==========================================================
# Text Splitter
# ==========================================================

SPLITTER = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
)

CHUNKS = SPLITTER.split_documents(DOCUMENTS)


# ==========================================================
# HuggingFace Embeddings
# ==========================================================

EMBEDDINGS = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL
)


# ==========================================================
# FAISS Vector Store
# ==========================================================

VECTOR_STORE = FAISS.from_documents(
    CHUNKS,
    EMBEDDINGS,
)

RETRIEVER = VECTOR_STORE.as_retriever(
    search_kwargs={
        "k": TOP_K
    }
)


# ==========================================================
# Prompt
# ==========================================================

RAG_PROMPT = ChatPromptTemplate.from_template(
    """
You are SmartKart AI Customer Support Assistant.

Answer ONLY using the provided context.

Guidelines:

- Never invent information.
- If the answer is unavailable in the context,
  politely inform the customer.
- Keep the response concise,
  professional and helpful.

Context:
{context}

Customer Question:
{question}
"""
)


# ==========================================================
# Global RAG Chain
# ==========================================================

RAG_CHAIN = (
    RAG_PROMPT
    | llm
    | StrOutputParser()
)


# ==========================================================
# Format Documents
# ==========================================================

def format_docs(
    documents: List[Document]
) -> str:
    """
    Converts retrieved LangChain documents
    into a single context string.
    """

    return "\n\n".join(
        document.page_content
        for document in documents
    )


# ==========================================================
# Ask RAG
# ==========================================================

def ask_rag(question: str) -> str:
    """
    Retrieves relevant SmartKart policy documents
    using FAISS and generates an answer using Gemini.
    """

    try:

        retrieved_docs = RETRIEVER.invoke(question)

        context = format_docs(retrieved_docs)

        response = RAG_CHAIN.invoke(
            {
                "context": context,
                "question": question,
            }
        )

        return response

    except Exception:

        return (
            "Sorry, I couldn't access the "
            "SmartKart knowledge base at the moment."
        )