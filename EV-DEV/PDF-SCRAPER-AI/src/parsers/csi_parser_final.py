"""
CSI MasterFormat parser - using word-level extraction to avoid cut-off titles.
"""
import re
from typing import List, Tuple, Optional
from loguru import logger
import pdfplumber


class CSIParser:
    """
    Intelligent parser for CSI MasterFormat PDFs using word-level column detection.
    """
    
    CODE_PATTERN = re.compile(r'^(\d{2})\s+(\d{2})\s+(\d{2})\s+(.+)$')
    DIVISION_PATTERN = re.compile(r'^DIVISION\s+(\d{2})—(.+)$')
    GROUP_PATTERN = re.compile(r'^(.+)\s+(Group|Subgroup)$')
    FOOTER_PATTERN = re.compile(r'CSI grants to .+ a non-exclusive')
    
    def __init__(self, column_split_x: float = 320.0):
        """
        Initialize parser with column split X position.
        
        Args:
            column_split_x: X-coordinate that separates left and right columns
        """
        self.current_group = None
        self.current_subgroup = None
        self.current_division = None
        self.column_split_x = column_split_x
        
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
    
    def extract_column_lines(self, page, max_x: float) -> List[str]:
        """
        Extract lines from page where text starts before max_x.
        This captures complete words/lines that start in the column.
        """
        words = page.extract_words(x_tolerance=3, y_tolerance=3)
        
        # Group words by line (similar y-coordinates)
        lines_dict = {}
        for word in words:
            if word['x0'] < max_x:  # Word starts in this column
                y = round(word['top'], 1)  # Round to group by line
                if y not in lines_dict:
                    lines_dict[y] = []
                lines_dict[y].append(word)
        
        # Sort by y-coordinate and build lines
        lines = []
        for y in sorted(lines_dict.keys()):
            # Sort words in line by x-coordinate
            line_words = sorted(lines_dict[y], key=lambda w: w['x0'])
            line_text = ' '.join(w['text'] for w in line_words)
            if line_text.strip() and not self.is_footer(line_text):
                lines.append(line_text.strip())
        
        return lines
    
    def extract_columns(self, page) -> Tuple[List[str], List[str]]:
        """Extract left and right columns using word-level detection."""
        words = page.extract_words(x_tolerance=3, y_tolerance=3)
        
        # Separate words into columns
        left_words = [w for w in words if w['x0'] < self.column_split_x]
        right_words = [w for w in words if w['x0'] >= self.column_split_x]
        
        def words_to_lines(word_list):
            lines_dict = {}
            for word in word_list:
                y = round(word['top'], 1)
                if y not in lines_dict:
                    lines_dict[y] = []
                lines_dict[y].append(word)
            
            lines = []
            for y in sorted(lines_dict.keys()):
                line_words = sorted(lines_dict[y], key=lambda w: w['x0'])
                line_text = ' '.join(w['text'] for w in line_words)
                if line_text.strip() and not self.is_footer(line_text):
                    lines.append(line_text.strip())
            return lines
        
        return words_to_lines(left_words), words_to_lines(right_words)
    
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
        """Parse a single PDF page using word-level extraction."""
        # Extract columns
        left_col, right_col = self.extract_columns(page)
        
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
