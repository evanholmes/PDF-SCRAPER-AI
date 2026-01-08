"""
CSI MasterFormat parser - using bbox-based column extraction.
"""
import re
from typing import List, Tuple, Optional
from loguru import logger
import pdfplumber


class CSIParser:
    """
    Intelligent parser for CSI MasterFormat PDFs using bbox-based column detection.
    """
    
    CODE_PATTERN = re.compile(r'^(\d{2})\s+(\d{2})\s+(\d{2})\s+(.+)$')
    DIVISION_PATTERN = re.compile(r'^DIVISION\s+(\d{2})—(.+)$')
    GROUP_PATTERN = re.compile(r'^(.+)\s+(Group|Subgroup)$')
    FOOTER_PATTERN = re.compile(r'CSI grants to .+ a non-exclusive')
    
    def __init__(self, left_bbox=(0, 0, 300, 800), right_bbox=(300, 0, 612, 800)):
        """
        Initialize parser with column bounding boxes.
        
        Args:
            left_bbox: (x0, top, x1, bottom) for left column
            right_bbox: (x0, top, x1, bottom) for right column
        """
        self.current_group = None
        self.current_subgroup = None
        self.current_division = None
        self.left_bbox = left_bbox
        self.right_bbox = right_bbox
        
    def is_footer(self, line: str) -> bool:
        """Check if line is part of footer."""
        return bool(self.FOOTER_PATTERN.search(line)) or (line.strip().isdigit() and len(line.strip()) <= 3)
    
    def is_code_line(self, line: str) -> bool:
        """Check if line starts with a valid code."""
        return bool(re.match(r'^\d{2}\s+\d{2}\s+\d{2}\s+', line))
    
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
            code = f"{match.group(2)} {match.group(3)}"  # Just the 6-digit code
            title = match.group(4).strip()
            return (div, code, title)
        return None
    
    def extract_column_text(self, page, bbox) -> List[str]:
        """Extract text from a specific bounding box (column)."""
        cropped = page.crop(bbox)
        text = cropped.extract_text()
        if not text:
            return []
        
        lines = []
        for line in text.split('\n'):
            line = line.strip()
            if line and not self.is_footer(line):
                lines.append(line)
        return lines
    
    def merge_multiline_titles(self, lines: List[str]) -> List[Tuple[str, str, str]]:
        """
        Merge multi-line titles into complete entries.
        
        Rule: Each entry starts with XX XX XX pattern.
        Lines without codes are continuations.
        """
        entries = []
        current_entry = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Skip headers
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
        """Parse a single PDF page using bbox-based column extraction."""
        # Extract each column separately
        left_col = self.extract_column_text(page, self.left_bbox)
        right_col = self.extract_column_text(page, self.right_bbox)
        
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
