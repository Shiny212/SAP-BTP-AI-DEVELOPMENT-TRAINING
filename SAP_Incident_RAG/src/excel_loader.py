"""
excel_loader.py

Enterprise Excel loader for the SAP Incident Knowledge Assistant.

Responsibilities
----------------
1. Load Excel dataset
2. Validate required columns
3. Display dataset summary
4. Explore dataset
5. Raise meaningful exceptions

Author : Shiny Belsiya
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import EXCEL_FILE, LINE
from src.logger import logger


class ExcelLoader:
    """
    Loads and validates the SAP Incident dataset.
    """

    REQUIRED_COLUMNS = [
        "incident_id",
        "incident_date",
        "sap_module",
        "category",
        "priority",
        "issue_summary",
        "issue_description",
        "root_cause",
        "resolution",
        "owner_team",
        "resolution_time_hours",
        "status",
    ]

    def __init__(self, file_path: Path = EXCEL_FILE):

        self.file_path = Path(file_path)

    def load(self) -> pd.DataFrame:
        """
        Load the Excel dataset.

        Returns
        -------
        pandas.DataFrame
        """

        logger.info("Loading Excel dataset...")

        if not self.file_path.exists():

            raise FileNotFoundError(
                f"Dataset not found:\n{self.file_path}"
            )

        dataframe = pd.read_excel(self.file_path)

        logger.info(
            "Dataset loaded successfully (%s rows).",
            len(dataframe),
        )

        return dataframe

    def validate_columns(
        self,
        dataframe: pd.DataFrame,
    ) -> None:
        """
        Validate dataset schema.
        """

        missing = [
            column
            for column in self.REQUIRED_COLUMNS
            if column not in dataframe.columns
        ]

        if missing:

            raise ValueError(
                f"Missing required columns:\n{missing}"
            )

        logger.info("Dataset schema validated.")

    @staticmethod
    def dataset_summary(
        dataframe: pd.DataFrame,
    ) -> None:

        print("\n" + LINE)
        print("DATASET SUMMARY")
        print(LINE)

        print(f"Rows               : {dataframe.shape[0]}")
        print(f"Columns            : {dataframe.shape[1]}")
        print(f"Duplicate Rows     : {dataframe.duplicated().sum()}")
        print(
            f"Memory Usage (KB)  : "
            f"{round(dataframe.memory_usage(deep=True).sum()/1024,2)}"
        )

    @staticmethod
    def show_head(
        dataframe: pd.DataFrame,
        rows: int = 5,
    ) -> None:

        print("\n" + LINE)
        print(f"FIRST {rows} RECORDS")
        print(LINE)

        print(dataframe.head(rows))

    @staticmethod
    def show_columns(
        dataframe: pd.DataFrame,
    ) -> None:

        print("\n" + LINE)
        print("COLUMN NAMES")
        print(LINE)

        for column in dataframe.columns:

            print(f"• {column}")

    @staticmethod
    def show_dtypes(
        dataframe: pd.DataFrame,
    ) -> None:

        print("\n" + LINE)
        print("DATA TYPES")
        print(LINE)

        print(dataframe.dtypes)

    @staticmethod
    def missing_values(
        dataframe: pd.DataFrame,
    ) -> None:

        print("\n" + LINE)
        print("MISSING VALUES")
        print(LINE)

        print(dataframe.isna().sum())

    @staticmethod
    def module_distribution(
        dataframe: pd.DataFrame,
    ) -> None:

        print("\n" + LINE)
        print("INCIDENTS BY SAP MODULE")
        print(LINE)

        print(
            dataframe["sap_module"]
            .value_counts()
            .sort_index()
        )

    @staticmethod
    def priority_distribution(
        dataframe: pd.DataFrame,
    ) -> None:

        print("\n" + LINE)
        print("INCIDENTS BY PRIORITY")
        print(LINE)

        print(
            dataframe["priority"]
            .value_counts()
            .sort_index()
        )