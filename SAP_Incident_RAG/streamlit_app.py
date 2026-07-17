"""
streamlit_app.py

SAP Incident Knowledge Assistant
Streamlit User Interface

Author : Shiny Belsiya
"""

from src.chunker import DocumentChunker
from src.data_cleaner import DataCleaner
from src.document_builder import DocumentBuilder
from src.excel_loader import ExcelLoader
from src.rag_pipeline import SAPIncidentRAG

import streamlit as st


# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="SAP Incident Knowledge Assistant",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 SAP Incident Knowledge Assistant")

st.markdown(
    "Ask questions about SAP incidents using Gemini-powered RAG."
)

# ---------------------------------------------------------
# Cache RAG Initialization
# ---------------------------------------------------------

@st.cache_resource
def load_rag():

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

    return rag


rag = load_rag()

st.success(
    f"Vector Database Loaded ({rag.retriever.vector_store.count()} incidents)"
)

# ---------------------------------------------------------
# User Input
# ---------------------------------------------------------

question = st.text_input(
    "Ask a Question",
    placeholder="Example: Supplier invoice blocked because of price variance",
)

# ---------------------------------------------------------
# Ask Button
# ---------------------------------------------------------

if st.button("Ask Gemini"):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner("Searching SAP Knowledge Base..."):

            answer = rag.ask(question)

        st.subheader("Answer")

        st.write(answer)