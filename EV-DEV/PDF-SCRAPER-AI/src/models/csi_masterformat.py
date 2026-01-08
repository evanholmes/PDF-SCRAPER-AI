"""
Data models for CSI MasterFormat 2020 parsing.
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
import re


class CSICode(BaseModel):
    """Represents a single CSI MasterFormat code entry."""

    division: str = Field(..., description="2-digit division number (e.g., '00', '01', '13')")
    code: str = Field(..., description="8-digit code with spaces (e.g., '00 11 00')")
    title: str = Field(..., description="Full title of the code entry")
    level: int = Field(default=2, description="Hierarchy level (typically 2 for Level 2 codes)")
    group: Optional[str] = Field(None, description="Parent group if applicable")
    subgroup: Optional[str] = Field(None, description="Parent subgroup if applicable")
    page_number: Optional[int] = Field(None, description="Source page number")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Parsing confidence score")

    @validator('division')
    def validate_division(cls, v):
        """Ensure division is 2 digits."""
        if not re.match(r'^\d{2}$', v):
            raise ValueError(f"Division must be 2 digits, got: {v}")
        return v

    @validator('code')
    def validate_code(cls, v):
        """Ensure code matches CSI format (4 or 6 digits: XX XX or XX XX XX)."""
        # Allow with or without spaces initially, normalize to spaced format
        normalized = re.sub(r'\s+', '', v)  # Remove all spaces

        if re.match(r'^\d{4}$', normalized):
            # 4-digit code: XX XX
            return f"{normalized[0:2]} {normalized[2:4]}"
        elif re.match(r'^\d{6}$', normalized):
            # 6-digit code: XX XX XX
            return f"{normalized[0:2]} {normalized[2:4]} {normalized[4:6]}"
        else:
            raise ValueError(f"Code must be 4 or 6 digits, got: {v}")

        return v

    @validator('title')
    def validate_title(cls, v):
        """Ensure title is not empty and properly formatted."""
        if not v or not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()

    def to_csv_row(self) -> List[str]:
        """Convert to CSV row format."""
        return [self.division, self.code, self.title, self.group or '', self.subgroup or '']

    def __str__(self):
        return f"{self.division} | {self.code} | {self.title}"


class CSIGroup(BaseModel):
    """Represents a CSI MasterFormat group."""
    name: str
    divisions: List[str] = Field(default_factory=list)


class CSISubgroup(BaseModel):
    """Represents a CSI MasterFormat subgroup."""
    name: str
    parent_group: str
    divisions: List[str] = Field(default_factory=list)


class ParsingResult(BaseModel):
    """Complete parsing result for a PDF."""
    codes: List[CSICode] = Field(default_factory=list)
    groups: List[CSIGroup] = Field(default_factory=list)
    subgroups: List[CSISubgroup] = Field(default_factory=list)
    total_codes: int = 0
    pages_processed: int = 0
    parsing_errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.now)
    quality_score: float = Field(default=0.0, ge=0.0, le=1.0)

    def add_code(self, code: CSICode):
        """Add a code and update counts."""
        self.codes.append(code)
        self.total_codes = len(self.codes)

    def to_csv(self) -> str:
        """Export to CSV format."""
        rows = [["Division", "Code", "Title", "Group", "Subgroup"]]
        rows.extend([code.to_csv_row() for code in self.codes])
        return '\n'.join([','.join(row) for row in rows])
