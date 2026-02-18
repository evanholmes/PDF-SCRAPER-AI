"""
CSI MasterFormat parser - handles two-column layout and multi-line titles.
"""
import re
from typing import List, Tuple, Optional
from loguru import logger
import pdfplumber


class CSIParser:
    """
    Intelligent parser for CSI MasterFormat PDFs.

    Handles:
    - Two-column layout detection
    - Multi-line title concatenation
    - Footer removal
    - Group/Subgroup tracking
    """

    # Patterns
    CODE_PATTERN = re.compile(r'^(\d{2})\s+(\d{2})\s+(\d{2})\s+(.+)$')
    DIVISION_PATTERN = re.compile(r'^DIVISION\s+(\d{2})—(.+)$')
    GROUP_PATTERN = re.compile(r'^(.+)\s+(Group|Subgroup)$')
    FOOTER_PATTERN = re.compile(r'CSI grants to .+ a non-exclusive')

    def __init__(self, column_split_pos: int = 48):
        self.current_group = None
        self.current_subgroup = None
        self.current_division = None
        self.column_split_pos = column_split_pos

    def is_footer(self, line: str) -> bool:
        """Check if line is part of footer."""
        return bool(self.FOOTER_PATTERN.search(line)) or line.strip().isdigit()

    def is_code_line(self, line: str) -> bool:
        """Check if line starts with a valid code (XX XX XX pattern)."""
        return bool(re.match(r'^\d{2}\s+\d{2}\s+\d{2}\s+\d{2}\s+', line))

    def is_division_header(self, line: str) -> bool:
        """Check if line is a division header."""
        return bool(self.DIVISION_PATTERN.match(line))

    def is_group_header(self, line: str) -> bool:
        """Check if line is a group/subgroup header."""
        return bool(self.GROUP_PATTERN.match(line))

    def extract_code_parts(self, line: str) -> Optional[Tuple[str, str, str]]:
        """
        Extract division, code (6 digits), and title from a code line.
        Format: XX XX XX (6 digits) - division is first 2 digits
        Returns: (division, code, title) or None
        """
        match = self.CODE_PATTERN.match(line)
        if match:
            div = match.group(1)
            code = f"{match.group(2)} {match.group(3)}"  # Just the 6-digit code (XX XX XX)
            title = match.group(4).strip()
            return (div, code, title)
        return None

    def parse_two_column_layout(self, text: str) -> Tuple[List[str], List[str]]:
        """
        Parse two-column PDF layout into separate left and right columns.

        Strategy:
        1. Extract text with layout preservation
        2. Split at character position ~50 (middle of page)
        3. Return left column, then right column
        """
        lines = text.split('\n')

        left_column = []
        right_column = []

        for line in lines:
            if self.is_footer(line):
                break

            if not line.strip():
                continue

            # Extract left column (positions 0 to split_pos)
            left_text = line[:self.column_split_pos].strip()
            # Extract right column (positions split_pos onward)
            right_text = line[self.column_split_pos:].strip()

            if left_text:
                left_column.append(left_text)
            if right_text:
                right_column.append(right_text)

        return left_column, right_column

    def merge_multiline_titles(self, lines: List[str]) -> List[Tuple[str, str, str]]:
        """
        Merge multi-line titles into single entries.

        Rules:
        - Each entry MUST start with XX XX XX XX pattern
        - Lines without codes are continuations of previous title
        - Stop merging when next code line is found

        Returns: List of (division, code, full_title) tuples
        """
        entries = []
        current_entry = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check if this is a code line
            parts = self.extract_code_parts(line)

            if parts:
                # Save previous entry if exists
                if current_entry:
                    entries.append(current_entry)
                # Start new entry
                current_entry = parts
            else:
                # This is a continuation line
                if current_entry:
                    div, code, title = current_entry
                    # Append to title
                    current_entry = (div, code, f"{title} {line}")

        # Add final entry
        if current_entry:
            entries.append(current_entry)

        return entries

    def parse_page(self, page_text: str, page_num: int) -> List[dict]:
        """
        Parse a single page of CSI MasterFormat PDF.

        Returns: List of code dictionaries
        """
        # Step 1: Split into left and right columns
        left_col, right_col = self.parse_two_column_layout(page_text)
        all_lines = left_col + right_col

        # Step 2: Track group/subgroup/division context
        for line in all_lines:
            if self.is_division_header(line):
                match = self.DIVISION_PATTERN.match(line)
                if match:
                    self.current_division = match.group(1)
                    logger.debug(f"Found division: {self.current_division} - {match.group(2)}")

            elif self.is_group_header(line):
                # Update current group/subgroup
                if "Subgroup" in line:
                    self.current_subgroup = line.replace("Subgroup", "").strip()
                else:
                    self.current_group = line.replace("Group", "").strip()
                    self.current_subgroup = None

        # Step 3: Extract and merge code entries from each column separately
        left_entries = self.merge_multiline_titles(left_col)
        right_entries = self.merge_multiline_titles(right_col)
        all_entries = left_entries + right_entries

        # Step 4: Build result dictionaries
        results = []
        for div, code, title in all_entries:
            results.append({
                'division': div,
                'code': code,
                'title': title,
                'group': self.current_group,
                'subgroup': self.current_subgroup,
                'page_number': page_num
            })

        return results

    def parse_pdf(self, pdf_path: str) -> List[dict]:
        """
        Parse entire CSI MasterFormat PDF.

        Returns: List of all extracted codes
        """
        logger.info(f"Parsing PDF: {pdf_path}")
        all_codes = []

        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                logger.debug(f"Processing page {page_num + 1}/{len(pdf.pages)}")
                text = page.extract_text(layout=True)  # Preserve layout for column detection
                if text:
                    codes = self.parse_page(text, page_num + 1)
                    all_codes.extend(codes)
                    logger.debug(f"Extracted {len(codes)} codes from page {page_num + 1}")

        logger.info(f"Total codes extracted: {len(all_codes)}")
        return all_codes
