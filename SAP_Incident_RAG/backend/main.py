"""
main.py

FastAPI Backend

Author : Shiny Belsiya
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.chunker import DocumentChunker
from src.data_cleaner import DataCleaner
from src.document_builder import DocumentBuilder
from src.excel_loader import ExcelLoader
from src.rag_pipeline import SAPIncidentRAG

from backend.schemas import (
    QuestionRequest,
    QuestionResponse,
)

app = FastAPI(
    title="SAP Incident Knowledge Assistant API",
    version="1.0.0",
)

# ---------------------------------------------------------
# Enable CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# Initialize RAG
# ---------------------------------------------------------

loader = ExcelLoader()

cleaner = DataCleaner()

builder = DocumentBuilder()

chunker = DocumentChunker()

rag = SAPIncidentRAG()

dataframe = loader.load()

loader.validate_columns(dataframe)

dataframe = cleaner.clean(dataframe)

documents = builder.build_documents(dataframe)

chunks = chunker.split_documents(documents)

rag.initialize(chunks)

# ---------------------------------------------------------
# Routes
# ---------------------------------------------------------


@app.get("/")
def home():

    return {
        "message": "SAP Incident Knowledge Assistant API Running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy",
        "vectors": rag.retriever.vector_store.count(),
    }


@app.post(
    "/ask",
    response_model=QuestionResponse,
)
def ask_question(
    request: QuestionRequest,
):

    answer = rag.ask(request.question)

    return QuestionResponse(
        answer=answer,
    )