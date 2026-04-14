"""
PDF text extraction module for sustainability reports.

This module extracts text content from PDF files using PyMuPDF (fitz).
"""

import fitz  # PyMuPDF
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class PDFExtractor:
    """Extract text content from PDF files."""

    def __init__(self):
        """Initialize PDF extractor."""
        self.logger = logger

    def extract_text(self, pdf_path: str) -> Optional[str]:
        """
        Extract all text from a PDF file.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Extracted text or None if extraction fails
        """
        try:
            document = fitz.open(pdf_path)
            text = ""

            for page_num in range(len(document)):
                page = document[page_num]
                text += f"\n--- Page {page_num + 1} ---\n"
                text += page.get_text()

            document.close()
            self.logger.info(f"Successfully extracted text from {pdf_path}")
            return text

        except FileNotFoundError:
            self.logger.error(f"PDF file not found: {pdf_path}")
            return None
        except Exception as e:
            self.logger.error(f"Error extracting text from PDF: {str(e)}")
            return None

    def extract_text_by_page(self, pdf_path: str) -> Optional[dict]:
        """
        Extract text from PDF organized by page.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Dictionary with page numbers as keys and text as values
        """
        try:
            document = fitz.open(pdf_path)
            pages_text = {}

            for page_num in range(len(document)):
                page = document[page_num]
                pages_text[page_num + 1] = page.get_text()

            document.close()
            self.logger.info(f"Successfully extracted text by page from {pdf_path}")
            return pages_text

        except Exception as e:
            self.logger.error(f"Error extracting text by page: {str(e)}")
            return None
