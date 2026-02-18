import pdfplumber
import sys

pdf_path = sys.argv[1]
page_num = int(sys.argv[2]) if len(sys.argv) > 2 else 0

with pdfplumber.open(pdf_path) as pdf:
    print(f"Total pages: {len(pdf.pages)}")
    print(f"\n--- Page {page_num + 1} Analysis ---")
    page = pdf.pages[page_num]
    print(f"Page size: {page.width} x {page.height}")
    
    # Extract text
    text = page.extract_text()
    print(f"\n--- First 1000 characters of text ---")
    print(text[:1000] if text else "No text extracted")
    
    # Check for tables
    tables = page.extract_tables()
    print(f"\n--- Tables found: {len(tables)} ---")
    if tables:
        print(f"First table preview (first 5 rows):")
        for i, row in enumerate(tables[0][:5]):
            print(row)
