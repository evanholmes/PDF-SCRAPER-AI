import pdfplumber

with pdfplumber.open("data/input/MasterFormat_2020 - pgs_17-39 - MasterFormat Groups, Subgroups, and Divisions.pdf") as pdf:
    page = pdf.pages[2]
    
    # Get character-level positions
    chars = page.chars
    
    # Find x-positions where codes start
    code_x_positions = []
    for char in chars:
        text = char.get('text', '')
        if text.isdigit():
            x = char.get('x0')
            code_x_positions.append(x)
    
    # Find clusters (left column vs right column)
    if code_x_positions:
        import statistics
        sorted_x = sorted(set(code_x_positions))
        print(f"Unique X positions: {sorted_x[:20]}")
        print(f"Min X: {min(sorted_x)}, Max X: {max(sorted_x)}")
        
        # Find gap between columns
        gaps = [(sorted_x[i+1], sorted_x[i+1] - sorted_x[i]) for i in range(len(sorted_x)-1)]
        largest_gap = max(gaps, key=lambda x: x[1])
        print(f"\nLargest gap at X={largest_gap[0]}, size={largest_gap[1]}")
