import pdfplumber

with pdfplumber.open("data/input/MasterFormat_2020 - pgs_17-39 - MasterFormat Groups, Subgroups, and Divisions.pdf") as pdf:
    page = pdf.pages[2]  # Page 3 with data
    
    # Try extracting with layout preservation
    text = page.extract_text(layout=True)
    
    print("=== RAW TEXT WITH LAYOUT ===")
    lines = text.split('\n')
    for i, line in enumerate(lines[0:40]):
        print(f"{i+1:3d}: |{line}|")
