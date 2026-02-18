import pdfplumber

with pdfplumber.open("data/input/MasterFormat_2020 - pgs_17-39 - MasterFormat Groups, Subgroups, and Divisions.pdf") as pdf:
    page = pdf.pages[2]
    text = page.extract_text()
    lines = text.split('\n')
    
    print(f"Total lines: {len(lines)}")
    print("\n--- First 30 lines ---")
    for i, line in enumerate(lines[:30]):
        print(f"{i+1:3d}: {line}")
    
    print("\n--- Last 10 lines (footer) ---")
    for i, line in enumerate(lines[-10:]):
        print(f"{len(lines)-10+i+1:3d}: {line}")
