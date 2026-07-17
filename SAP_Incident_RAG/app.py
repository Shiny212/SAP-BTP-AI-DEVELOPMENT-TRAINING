"""
app.py

Main entry point for the
SAP Incident Knowledge Assistant.

Author : Shiny Belsiya
"""

from src.chunker import DocumentChunker
from src.data_cleaner import DataCleaner
from src.document_builder import DocumentBuilder
from src.excel_loader import ExcelLoader
from src.rag_pipeline import SAPIncidentRAG


def main() -> None:
    """
    Execute the complete SAP Incident RAG workflow.
    """

    # ---------------------------------------------------------
    # Initialize Components
    # ---------------------------------------------------------

    loader = ExcelLoader()

    cleaner = DataCleaner()

    builder = DocumentBuilder()

    chunker = DocumentChunker()

    rag = SAPIncidentRAG()

    # ---------------------------------------------------------
    # Load Dataset
    # ---------------------------------------------------------

    dataframe = loader.load()

    loader.validate_columns(dataframe)

    # ---------------------------------------------------------
    # Clean Dataset
    # ---------------------------------------------------------

    dataframe = cleaner.clean(dataframe)

    # ---------------------------------------------------------
    # Build Documents
    # ---------------------------------------------------------

    documents = builder.build_documents(dataframe)

    # ---------------------------------------------------------
    # Chunk Documents
    # ---------------------------------------------------------

    chunks = chunker.split_documents(documents)

    # ---------------------------------------------------------
    # Initialize Vector Store
    # ---------------------------------------------------------

    rag.initialize(chunks)

    print("\n")
    print("=" * 90)
    print("SAP INCIDENT KNOWLEDGE ASSISTANT")
    print("=" * 90)

    print(f"\nVector Count : {rag.retriever.vector_store.count()}")

    # ---------------------------------------------------------
    # Interactive Question Loop
    # ---------------------------------------------------------

    while True:

        print()

        question = input(
            "Ask your SAP Incident Question (type 'exit' to quit): "
        ).strip()

        if question.lower() == "exit":

            print("\nGoodbye!")

            break

        if not question:

            print("Please enter a valid question.")

            continue

        answer = rag.ask(question)

        print("\n")
        print("=" * 90)
        print("ANSWER")
        print("=" * 90)

        print(answer)


if __name__ == "__main__":

    main()