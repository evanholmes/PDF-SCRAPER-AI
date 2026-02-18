"""
CSI MasterFormat parser v2 - properly handles two-column layout.
"""
import re
from typing import List, Tuple, Optional
from loguru import logger
import pdfplumber


class CSIParser:
    """
    Intelligent parser for CSI MasterFormat PDFs with proper two-column handling.
    """
    
    CODE_PATTERN = re.compile(r'^(\d{2})\s+(\d{2})\s+(\d{2})\s+(\d{2})\s+(.+)$')
    DIVISION_PATTERN = re.compile(r'^DIVISION\s+(\d{2})—(.+)$')
    GROUP_PATTERN = re.compile(r'^(.+)\s+(Group|Subgroup)$')
    FOOTER_PATTERN = re.compile(r'CSI grants to .+ a non-exclusive')
    
    def __init__(self, column_split_pos: int = 50):
        self.current_group = None
        self.current_subgroup = None
        self.current_division = None
        self.column_split_pos = column_split_pos
        
    def is_footer(self, line: str) -> bool:
        """Check if line is part of footer."""
        return bool(self.FOOTER_PATTERN.search(line)) or (line.strip().isdigit() and len(line.strip()) <= 3)
    
    def is_code_line(self, line: str) -> bool:
        """Check if line starts with a valid code."""
        return bool(re.match(r'^\d{2}\s+\d{2}\s+\d{2}\s+\d{2}\s+', line))
    
    def is_division_header(self, line: str) -> bool:
        """Check if line is a division header."""
        return bool(self.DIVISION_PATTERN.match(line))
    
    def is_group_header(self, line: str) -> bool:
        """Check if line is a group/subgroup header."""
        return bool(self.GROUP_PATTERN.match(line))
    
    def extract_code_parts(self, line: str) -> Optional[Tuple[str, str, str]]:
        """Extract division, code, and title from a code line."""
        match = self.CODE_PATTERN.match(line)
        if match:
            div = match.group(1)
            code = f"{match.group(1)} {match.group(2)} {match.group(3)} {match.group(4)}"
            title = match.group(5).strip()
            return (div, code, title)
        return None
    
    def split_columns(self, text: str) -> Tuple[List[str], List[str]]:
        """
        Split two-column layout into separate left and right columns.
        """
        lines = text.split('\n')
        
        left_column = []
        right_column = []
        
        for line in lines:
            if self.is_footer(line):
                break
                
            # Skip empty lines
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
        Merge multi-line titles into complete entries.
        
        Rule: Each entry starts with XX XX XX XX pattern.
        Lines without codes are continuations.
        """
        entries = []
        current_entry = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Skip headers and non-code lines that shouldn't be merged
            if self.is_division_header(line) or self.is_group_header(line):
                continue
            
            parts = self.extract_code_parts(line)
            
            if parts:
                # Save previous entry
                if current_entry:
                    entries.append(current_entry)
                # Start new entry
                current_entry = parts
            else:
                # Continuation line
                if current_entry and not line.startswith('DIVISION'):
                    div, code, title = current_entry
                    current_entry = (div, code, f"{title} {line}")
        
        # Add final entry
        if current_entry:
            entries.append(current_entry)
        
        return entries
    
    def update_context(self, lines: List[str]):
        """Update group/subgroup/division context from lines."""
        for line in lines:
            if self.is_division_header(line):
                match = self.DIVISION_PATTERN.match(line)
                if match:
                    self.current_division = match.group(1)
                    logger.debug(f"Division: {self.current_division} - {match.group(2)}")
            
            elif self.is_group_header(line):
                if "Subgroup" in line:
                    self.current_subgroup = line.replace("Subgroup", "").strip()
                    logger.debug(f"Subgroup: {self.current_subgroup}")
                else:
                    self.current_group = line.replace("Group", "").strip()
                    self.current_subgroup = None
                    logger.debug(f"Group: {self.current_group}")
    
    def parse_page(self, page, page_num: int) -> List[dict]:
        """Parse a single PDF page."""
        # Extract text with layout preserved
        text = page.extract_text(layout=True)
        if not text:
            return []
        
        # Split into columns
        left_col, right_col = self.split_columns(text)
        
        # Update context from both columns
        self.update_context(left_col + right_col)
        
        # Parse each column separately
        left_entries = self.merge_multiline_titles(left_col)
        right_entries = self.merge_multiline_titles(right_col)
        
        # Combine entries
        all_entries = left_entries + right_entries
        
        # Build result dictionaries
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
        """Parse entire CSI MasterFormat PDF."""
        logger.info(f"Parsing: {pdf_path}")
        all_codes = []
        
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                logger.debug(f"Page {page_num + 1}/{len(pdf.pages)}")
                codes = self.parse_page(page, page_num + 1)
                all_codes.extend(codes)
                if codes:
                    logger.debug(f"Extracted {len(codes)} codes")
        
        logger.info(f"Total: {len(all_codes)} codes")
        return all_codes
