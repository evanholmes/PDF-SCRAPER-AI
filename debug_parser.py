from src.parsers.csi_parser import CSIParser
from loguru import logger
import sys

logger.remove()
logger.add(sys.stdout, level="DEBUG")

parser = CSIParser()

import pdfplumber

with pdfplumber.open("data/input/MasterFormat_2020 - pgs_17-39 - MasterFormat Groups, Subgroups, and Divisions.pdf") as pdf:
    page = pdf.pages[2]  # Page 3
    text = page.extract_text(layout=True)
    
    left_col, right_col = parser.parse_two_column_layout(text)
    
    print("=== LEFT COLUMN (first 20 lines) ===")
    for i, line in enumerate(left_col[:20]):
        print(f"{i+1:3d}: {line}")
    
    print("\n=== RIGHT COLUMN (first 20 lines) ===")
    for i, line in enumerate(right_col[:20]):
        print(f"{i+1:3d}: {line}")
    
    print("\n=== Testing extract_code_parts ===")
    test_lines = [
        "01 58 00 Project Identification",
        "01 60 00 Product Requirements",
        "02 01 00 Maintenance of Existing"
    ]
    for line in test_lines:
        result = parser.extract_code_parts(line)
        print(f"'{line}' -> {result}")
