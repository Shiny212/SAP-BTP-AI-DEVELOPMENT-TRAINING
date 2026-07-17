"""
document_builder.py

Converts SAP Incident DataFrame into LangChain Documents.

Responsibilities
----------------
1. Convert each Excel row into a Document
2. Preserve metadata
3. Build clean searchable text
4. Validate required fields

Author : Shiny Belsiya
"""

from __future__ import annotations

from typing import List

import pandas as pd
from langchain_core.documents import Document

from src.logger import logger


class DocumentBuilder:
    """
    Build LangChain Document objects
    from SAP Incident records.
    """

    SEARCHABLE_COLUMNS = [
        "incident_id",
        "sap_module",
        "category",
        "priority",
        "issue_summary",
        "issue_description",
        "root_cause",
        "resolution",
        "owner_team",
        "status",
        "resolution_time_hours",
    ]

    @staticmethod
    def build_document_text(row: pd.Series) -> str:
        """
        Create searchable document text.
        """
        return f"""
SAP Incident Record

Incident ID: {row['incident_id']}

SAP Module: {row['sap_module']}

Category: {row['category']}

Priority: {row['priority']}

Issue Summary:
{row['issue_summary']}

Issue Description:
{row['issue_description']}

Root Cause:
{row['root_cause']}

Resolution:
{row['resolution']}

Owner Team:
{row['owner_team']}

Resolution Time:
{row['resolution_time_hours']} Hours

Status:
{row['status']}
""".strip()

    @staticmethod
    def build_metadata(
        row: pd.Series,
        row_number: int,
    ) -> dict:
        """
        Create metadata for filtering and citations.
        """

        return {
            "source_type": "excel",
            "source_name": "sap_incidents.xlsx",
            "sheet_name": "Sheet1",
            "row_number": row_number,

            "incident_id": row["incident_id"],
            "sap_module": row["sap_module"],
            "priority": row["priority"],
            "category": row["category"],
            "owner_team": row["owner_team"],
            "status": row["status"],
        }

    def build_documents(
        self,
        dataframe: pd.DataFrame,
    ) -> List[Document]:
        """
        Convert DataFrame into LangChain Documents.
        """

        logger.info("Building LangChain Documents...")

        documents: List[Document] = []

        for row_number, (_, row) in enumerate(
            dataframe.iterrows(),
            start=1,
        ):

            document = Document(
                page_content=self.build_document_text(row),
                metadata=self.build_metadata(
                    row,
                    row_number,
                ),
            )

            documents.append(document)

        logger.info(
            "%s Documents Created",
            len(documents),
        )

        return documents