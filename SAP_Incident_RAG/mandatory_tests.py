"""
mandatory_tests.py

Execute mandatory SAP Incident RAG test questions.

Author : Shiny Belsiya
"""

from src.chunker import DocumentChunker
from src.data_cleaner import DataCleaner
from src.document_builder import DocumentBuilder
from src.excel_loader import ExcelLoader
from src.rag_pipeline import SAPIncidentRAG


def main():

    print("=" * 90)
    print("SAP INCIDENT RAG - MANDATORY TESTS")
    print("=" * 90)

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

    print(f"\nVector Count : {rag.retriever.vector_store.count()}")

    test_cases = [

        {
            "question":
            "Supplier invoice blocked because of price variance"
        },

        {
            "question":
            "Pricing calculation incorrect"
        },

        {
            "question":
            "Purchase order release workflow failed"
        },

        {
            "question":
            "User authorization failed"
        },

        {
            "question":
            "Material master not found"
        },

    ]

    for index, test in enumerate(
        test_cases,
        start=1,
    ):

        print("\n")
        print("=" * 90)
        print(f"TEST CASE {index}")
        print("=" * 90)

        print("\nQuestion")

        print(test["question"])

        print("\nAnswer")

        answer = rag.ask(
            question=test["question"],
        )

        print(answer)

        print("\n")


if __name__ == "__main__":

    main()