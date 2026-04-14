"""
PDF table extraction module for sustainability reports.

This module extracts tables from PDF files using Camelot.
"""

import camelot
import pandas as pd
import logging
from typing import Optional, List

logger = logging.getLogger(__name__)


class TableExtractor:
    """Extract tables from PDF files."""

    def __init__(self):
        """Initialize table extractor."""
        self.logger = logger

    def extract_tables(self, pdf_path: str) -> Optional[List[pd.DataFrame]]:
        """
        Extract all tables from a PDF file.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            List of pandas DataFrames or None if extraction fails
        """
        try:
            # Extract tables using Camelot
            tables = camelot.read_pdf(
                pdf_path,
                pages="all",
                flavor="lattice",  # Use lattice detection
                suppress_stdout=True
            )

            if len(tables) == 0:
                # Try stream detection if lattice fails
                tables = camelot.read_pdf(
                    pdf_path,
                    pages="all",
                    flavor="stream",
                    suppress_stdout=True
                )

            dataframes = [table.df for table in tables]
            self.logger.info(f"Extracted {len(dataframes)} tables from {pdf_path}")
            return dataframes

        except Exception as e:
            self.logger.error(f"Error extracting tables: {str(e)}")
            return None

    def extract_tables_from_page(self, pdf_path: str, page_num: int) -> Optional[List[pd.DataFrame]]:
        """
        Extract tables from a specific page.

        Args:
            pdf_path: Path to the PDF file
            page_num: Page number (1-indexed)

        Returns:
            List of pandas DataFrames from the page
        """
        try:
            tables = camelot.read_pdf(
                pdf_path,
                pages=str(page_num),
                flavor="lattice",
                suppress_stdout=True
            )

            if len(tables) == 0:
                tables = camelot.read_pdf(
                    pdf_path,
                    pages=str(page_num),
                    flavor="stream",
                    suppress_stdout=True
                )

            dataframes = [table.df for table in tables]
            self.logger.info(f"Extracted {len(dataframes)} tables from page {page_num}")
            return dataframes

        except Exception as e:
            self.logger.error(f"Error extracting tables from page: {str(e)}")
            return None

    def save_tables_to_csv(self, pdf_path: str, output_dir: str) -> bool:
        """
        Extract tables and save them as CSV files.

        Args:
            pdf_path: Path to the PDF file
            output_dir: Directory to save CSV files

        Returns:
            True if successful, False otherwise
        """
        try:
            tables = self.extract_tables(pdf_path)
            if not tables:
                return False

            for i, df in enumerate(tables):
                output_path = f"{output_dir}/table_{i + 1}.csv"
                df.to_csv(output_path, index=False)
                self.logger.info(f"Saved table {i + 1} to {output_path}")

            return True

        except Exception as e:
            self.logger.error(f"Error saving tables to CSV: {str(e)}")
            return False
