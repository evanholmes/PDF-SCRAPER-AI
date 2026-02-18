from src.parsers.csi_parser_bbox import CSIParser
import pdfplumber

parser = CSIParser(
    left_bbox=(0, 0, 306, 792),
    right_bbox=(306, 0, 612, 792)
)

with pdfplumber.open("data/input/MasterFormat_2020 - pgs_17-39 - MasterFormat Groups, Subgroups, and Divisions.pdf") as pdf:
    page = pdf.pages[2]  # Page 3
    
    print("=== LEFT COLUMN ===")
    left_crop = page.crop((0, 0, 306, 792))
    left_text = left_crop.extract_text()
    for i, line in enumerate(left_text.split('\n')[:20]):
        print(f"{i+1:3d}: {line}")
    
    print("\n=== RIGHT COLUMN ===")
    right_crop = page.crop((306, 0, 612, 792))
    right_text = right_crop.extract_text()
    for i, line in enumerate(right_text.split('\n')[:20]):
        print(f"{i+1:3d}: {line}")
