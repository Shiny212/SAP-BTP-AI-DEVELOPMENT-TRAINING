"""
data_cleaner.py

Enterprise Data Cleaning Module
for SAP Incident Knowledge Assistant

Responsibilities
----------------
1. Remove duplicate records
2. Remove empty rows
3. Fill missing values
4. Convert date columns
5. Normalize text
6. Standardize priority
7. Standardize SAP modules
8. Convert numeric columns
9. Validate cleaned dataset

Author : Shiny Belsiya
"""

from __future__ import annotations

import pandas as pd

from src.logger import logger


class DataCleaner:
    """
    Cleans and standardizes the SAP Incident dataset.
    """

    TEXT_COLUMNS = [
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
    ]

    PRIORITY_MAP = {
        "P1": "P1",
        "P2": "P2",
        "P3": "P3",
        "P4": "P4",
        "HIGH": "P1",
        "MEDIUM": "P2",
        "LOW": "P3",
        "CRITICAL": "P1",
    }

    MODULE_MAP = {
        "HANA": "SAP HANA",
        "BTP": "SAP BTP",
        "SUCCESSFACTORS": "SAP SuccessFactors",
        "MM": "SAP MM",
        "SD": "SAP SD",
        "FI": "SAP FI",
        "CO": "SAP CO",
    }

    def clean(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Execute complete cleaning pipeline.
        """

        logger.info("Starting data cleaning...")

        df = dataframe.copy()

        df = self.remove_empty_rows(df)

        df = self.remove_duplicates(df)

        df = self.clean_text_columns(df)

        df = self.convert_dates(df)

        df = self.standardize_priority(df)

        df = self.standardize_modules(df)

        df = self.convert_numeric(df)

        df = self.fill_missing(df)

        logger.info("Data cleaning completed.")

        return df

    @staticmethod
    def remove_empty_rows(
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        return dataframe.dropna(how="all")

    @staticmethod
    def remove_duplicates(
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        return dataframe.drop_duplicates()

    def clean_text_columns(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        for column in self.TEXT_COLUMNS:

            dataframe[column] = (
                dataframe[column]
                .astype(str)
                .str.strip()
                .str.replace(r"\s+", " ", regex=True)
            )

        return dataframe

    @staticmethod
    def convert_dates(
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        dataframe["incident_date"] = pd.to_datetime(
            dataframe["incident_date"],
            errors="coerce",
        )

        return dataframe

    def standardize_priority(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        dataframe["priority"] = (
            dataframe["priority"]
            .str.upper()
            .map(self.PRIORITY_MAP)
            .fillna("P3")
        )

        return dataframe

    def standardize_modules(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        dataframe["sap_module"] = (
            dataframe["sap_module"]
            .replace(self.MODULE_MAP)
        )

        return dataframe

    @staticmethod
    def convert_numeric(
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        dataframe["resolution_time_hours"] = pd.to_numeric(
            dataframe["resolution_time_hours"],
            errors="coerce",
        )

        return dataframe

    @staticmethod
    def fill_missing(
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        text_columns = dataframe.select_dtypes(
            include="object"
        ).columns

        dataframe[text_columns] = dataframe[
            text_columns
        ].fillna("Not Available")

        dataframe["resolution_time_hours"] = (
            dataframe["resolution_time_hours"]
            .fillna(0)
        )

        return dataframe

    @staticmethod
    def summary(
        dataframe: pd.DataFrame,
    ) -> None:

        print("\n")
        print("=" * 90)
        print("CLEAN DATA SUMMARY")
        print("=" * 90)

        print(f"Rows      : {len(dataframe)}")
        print(f"Columns   : {len(dataframe.columns)}")
        print(
            f"Duplicates: {dataframe.duplicated().sum()}"
        )
        print(
            f"Missing   : {dataframe.isna().sum().sum()}"
        )