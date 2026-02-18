from src.parsers.csi_parser_bbox import CSIParser
import pdfplumber

# Try wider left column to capture full titles
parser = CSIParser(
    left_bbox=(0, 0, 340, 792),    # Wider to capture full left column titles
    right_bbox=(340, 0, 612, 792)  # Right column starts later
)

with pdfplumber.open("data/input/MasterFormat_2020 - pgs_17-39 - MasterFormat Groups, Subgroups, and Divisions.pdf") as pdf:
    page = pdf.pages[2]
    
    print("=== LEFT COLUMN (wider bbox) ===")
    left_crop = page.crop((0, 0, 340, 792))
    left_text = left_crop.extract_text()
    for i, line in enumerate(left_text.split('\n')[:20]):
        print(f"{i+1:3d}: {line}")
    
    print("\n=== RIGHT COLUMN ===")
    right_crop = page.crop((340, 0, 612, 792))
    right_text = right_crop.extract_text()
    for i, line in enumerate(right_text.split('\n')[:20]):
        print(f"{i+1:3d}: {line}")
