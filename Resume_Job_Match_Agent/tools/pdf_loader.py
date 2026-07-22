"""
tools/pdf_loader.py

PDF Resume Loader
"""

from __future__ import annotations

from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader


SUPPORTED_EXTENSIONS = {".pdf"}


def validate_pdf_file(file_path: str) -> None:
    """
    Validate whether the supplied file exists and is a PDF.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            "Only PDF files are supported."
        )


def load_pdf(file_path: str) -> List[Document]:
    """
    Load a PDF using LangChain's PyPDFLoader.

    Returns
    -------
    List[Document]
    """

    validate_pdf_file(file_path)

    loader = PyPDFLoader(file_path)

    return loader.load()


def extract_text(file_path: str) -> str:
    """
    Extract text from all pages of a PDF.
    """

    documents = load_pdf(file_path)

    pages = [
        document.page_content.strip()
        for document in documents
        if document.page_content.strip()
    ]

    return "\n\n".join(pages)


def extract_page_text(
    file_path: str,
    page_number: int,
) -> str:
    """
    Extract text from a specific page.

    Page numbering starts from 1.
    """

    documents = load_pdf(file_path)

    if page_number < 1:
        raise ValueError(
            "Page number must be greater than zero."
        )

    if page_number > len(documents):
        raise IndexError(
            "Page number exceeds total pages."
        )

    return documents[
        page_number - 1
    ].page_content.strip()


def get_total_pages(file_path: str) -> int:
    """
    Return total pages in the PDF.
    """

    documents = load_pdf(file_path)

    return len(documents)


def preview_pdf(
    file_path: str,
    characters: int = 500,
) -> str:
    """
    Return the first few characters of the resume.
    """

    text = extract_text(file_path)

    if len(text) <= characters:
        return text

    return text[:characters] + "..."


def pdf_summary(file_path: str) -> dict:
    """
    Return basic PDF information.
    """

    text = extract_text(file_path)

    return {
        "file_name": Path(file_path).name,
        "pages": get_total_pages(file_path),
        "characters": len(text),
        "words": len(text.split()),
    }