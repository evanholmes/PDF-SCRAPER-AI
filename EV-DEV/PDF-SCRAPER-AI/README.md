# PDF-SCRAPER-AI

**AI-Driven PDF Parsing Team - Zero-Error Extraction System**

## Mission

Parse dense, complex PDFs (600+ pages with cost codes, tables, forms) with 100% accuracy through multi-agent validation and auditing.

## Agent Team Structure

### Orchestrator (Lead Agent)
- Coordinates all parsing operations
- Distributes work to specialized agents
- Ensures quality gates are met
- Final decision authority

### Specialized Agents

1. **Extractor Agent**
   - Raw PDF text extraction (PyMuPDF, pdfplumber)
   - Table detection and extraction (Camelot, Tabula)
   - OCR for scanned documents (Tesseract)
   - Image extraction and analysis

2. **Validator Agent**
   - Schema validation
   - Data type checking
   - Completeness verification
   - Format consistency

3. **Auditor Agent**
   - Cross-reference verification
   - Mathematical validation (totals, subtotals)
   - Logical consistency checks
   - Pattern recognition for errors

4. **Quality Control Agent**
   - Final verification pass
   - Edge case detection
   - Confidence scoring
   - Error reporting

## Project Structure

```
PDF-SCRAPER-AI/
├── src/
│   ├── agents/          # Agent implementations
│   ├── parsers/         # PDF parsing engines
│   ├── validators/      # Validation logic
│   ├── models/          # Data models (Pydantic)
│   └── utils/           # Shared utilities
├── tests/               # Unit and integration tests
├── docs/
│   └── agents/          # Agent documentation
├── data/
│   ├── input/           # PDFs to process
│   ├── output/          # Parsed results
│   └── temp/            # Temporary processing files
├── logs/                # Execution logs
└── claude-prp-methodology/  # Development methodology

## Setup

1. **Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables**
   ```bash
   cp .env.example .env
   # Add your ANTHROPIC_API_KEY
   ```

## Usage

```bash
# Run parsing pipeline
python src/main.py --input data/input/document.pdf

# With full validation
python src/main.py --input document.pdf --validate-all

# Generate quality report
python src/main.py --input document.pdf --report
```

## Quality Gates

Every document passes through 4 validation levels:

1. **Level 1: Extraction Validation**
   - All pages extracted
   - No corrupted data
   - Character encoding correct

2. **Level 2: Structure Validation**
   - Tables properly detected
   - Headers/footers identified
   - Section boundaries clear

3. **Level 3: Content Validation**
   - Cost codes match expected format
   - Numbers parse correctly
   - Dates formatted properly
   - Cross-references valid

4. **Level 4: Audit Validation**
   - Mathematical totals correct
   - No duplicate entries
   - All required fields present
   - Confidence score > 95%

## Development

Built using the PRP (Product Requirement Prompt) methodology for systematic, validated development.

See `claude-prp-methodology/` for development workflow.

## License

MIT
