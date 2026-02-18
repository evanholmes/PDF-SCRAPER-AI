import pdfplumber

with pdfplumber.open("data/input/MasterFormat_2020 - pgs_17-39 - MasterFormat Groups, Subgroups, and Divisions.pdf") as pdf:
    page = pdf.pages[2]
    text = page.extract_text(layout=True)
    
    lines = text.split('\n')
    
    # Find lines with codes to determine column positions
    print("Looking for code patterns to find column split...")
    for i, line in enumerate(lines[5:30]):
        if any(line[j:j+8].replace(' ', '').isdigit() and len(line[j:j+8].replace(' ', '')) >= 6 
               for j in range(len(line)-8)):
            print(f"Line {i+5}: |{line}|")
            # Find where codes are
            for j in range(0, min(70, len(line)), 10):
                print(f"  Pos {j:2d}-{j+10:2d}: |{line[j:j+10]}|")
