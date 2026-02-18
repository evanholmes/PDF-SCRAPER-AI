from src.parsers.csi_parser_bbox import CSIParser
import pdfplumber

# Try giving left column more room
parser = CSIParser(
    left_bbox=(0, 0, 400, 792),    # Much wider
    right_bbox=(340, 0, 612, 792)  # Start at 340
)

with pdfplumber.open("data/input/MasterFormat_2020 - pgs_17-39 - MasterFormat Groups, Subgroups, and Divisions.pdf") as pdf:
    page = pdf.pages[2]
    
    print("=== LEFT COLUMN (very wide bbox) ===")
    left_crop = page.crop((0, 0, 400, 792))
    left_text = left_crop.extract_text()
    for i, line in enumerate(left_text.split('\n')[:25]):
        print(f"{i+1:3d}: |{line}|")
