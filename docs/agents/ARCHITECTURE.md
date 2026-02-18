# Agent Architecture

## Overview

The PDF-SCRAPER-AI system uses a multi-agent architecture where specialized agents work together under an orchestrator to achieve zero-error PDF parsing.

## Agent Communication Protocol

```
┌─────────────────┐
│  Orchestrator   │
│  (Lead Agent)   │
└────────┬────────┘
         │
    ┌────┴────┬────────┬──────────┐
    │         │        │          │
┌───▼───┐ ┌──▼───┐ ┌──▼────┐ ┌───▼────────┐
│Extract│ │Valid │ │Auditor│ │Quality Ctrl│
│Agent  │ │Agent │ │Agent  │ │   Agent    │
└───┬───┘ └──┬───┘ └──┬────┘ └───┬────────┘
    │        │        │          │
    └────────┴────────┴──────────┘
              Results Pool
```

## Agent Specifications

### 1. Orchestrator Agent

**Responsibilities:**
- Receive PDF input
- Distribute work to specialized agents
- Collect and synthesize results
- Make final parsing decisions
- Generate quality reports

**Decision Tree:**
```
PDF Input → Analyze complexity
         ├─ Simple (< 50 pages, text-only)
         │  └─ Direct Extractor → Validator → Output
         ├─ Medium (50-200 pages, some tables)
         │  └─ Extractor → Validator → Auditor → Output
         └─ Complex (200+ pages, dense tables/cost codes)
            └─ Full Pipeline (all 4 agents) → Output
```

### 2. Extractor Agent

**Responsibilities:**
- Multi-method PDF extraction
- Table detection and parsing
- OCR for scanned content
- Metadata extraction

**Tools:**
- PyMuPDF (fast text extraction)
- pdfplumber (table extraction)
- Camelot (complex table structures)
- Tesseract (OCR)

**Output Schema:**
```json
{
  "pages": [
    {
      "page_num": 1,
      "text": "...",
      "tables": [...],
      "images": [...],
      "metadata": {...}
    }
  ],
  "extraction_method": "hybrid",
  "confidence": 0.98
}
```

### 3. Validator Agent

**Responsibilities:**
- Schema validation against expected structure
- Data type verification
- Completeness checks
- Format standardization

**Validation Rules:**
```python
Rules = {
    "cost_codes": {
        "pattern": r"^\d{2}-\d{4}$",
        "required": True,
        "unique": True
    },
    "amounts": {
        "type": "decimal",
        "precision": 2,
        "required": True
    },
    "dates": {
        "format": "YYYY-MM-DD",
        "range": "valid_business_date"
    }
}
```

**Output:**
```json
{
  "valid": true,
  "errors": [],
  "warnings": ["Page 45: Date format inconsistent"],
  "validation_score": 0.99
}
```

### 4. Auditor Agent

**Responsibilities:**
- Cross-reference validation
- Mathematical verification (totals, subtotals)
- Logical consistency checks
- Pattern-based error detection

**Audit Checks:**
1. **Mathematical Integrity**
   - Sum of line items = section total
   - All subtotals = grand total
   - Percentages sum to 100%

2. **Cross-Reference Integrity**
   - Cost codes referenced exist
   - Page references valid
   - Section links consistent

3. **Pattern Analysis**
   - Detect anomalies (outliers in costs)
   - Flag suspicious duplicates
   - Identify missing sequences

**Output:**
```json
{
  "audit_passed": true,
  "findings": [
    {
      "type": "warning",
      "location": "Page 142, Line 23",
      "issue": "Cost code 45-1234 appears 3 times",
      "confidence": 0.85
    }
  ],
  "mathematical_verification": "passed",
  "audit_score": 0.97
}
```

### 5. Quality Control Agent

**Responsibilities:**
- Final verification pass
- Edge case detection
- Overall confidence scoring
- Error report generation

**Quality Metrics:**
```python
QualityScore = (
    extraction_confidence * 0.25 +
    validation_score * 0.25 +
    audit_score * 0.30 +
    consistency_score * 0.20
)

Threshold = 0.95  # Minimum acceptable quality
```

**Output:**
```json
{
  "quality_score": 0.98,
  "passed": true,
  "confidence_breakdown": {
    "extraction": 0.99,
    "validation": 0.98,
    "audit": 0.97,
    "consistency": 0.99
  },
  "recommendation": "approved",
  "review_required": false
}
```

## Error Handling Strategy

### Error Levels

1. **CRITICAL** - Stop processing, manual review required
   - Corrupted PDF
   - Unreadable pages
   - Security restrictions

2. **HIGH** - Agent retry with alternative method
   - Table extraction failed
   - OCR low confidence
   - Mathematical mismatch

3. **MEDIUM** - Flag for review, continue processing
   - Format inconsistency
   - Missing optional fields
   - Low confidence on specific sections

4. **LOW** - Log warning, continue
   - Formatting variations
   - Non-standard spacing
   - Minor metadata issues

### Retry Logic

```python
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(ExtractionError)
)
def extract_with_retry(pdf_path, method):
    # Try extraction
    # If fail, automatically retry with backoff
    pass
```

## Agent Development Guidelines

### Creating a New Agent

1. **Inherit from BaseAgent**
   ```python
   from src.agents.base import BaseAgent
   
   class NewAgent(BaseAgent):
       def process(self, input_data):
           # Implementation
           pass
   ```

2. **Implement Required Methods**
   - `process()` - Main processing logic
   - `validate_input()` - Input validation
   - `generate_output()` - Standardized output

3. **Add Logging**
   ```python
   from loguru import logger
   
   logger.info(f"Agent {self.name} started processing")
   ```

4. **Write Tests**
   ```python
   def test_new_agent():
       agent = NewAgent()
       result = agent.process(test_input)
       assert result.quality_score > 0.95
   ```

## Integration Points

### Orchestrator → Agent Communication

```python
# Orchestrator sends task
task = {
    "agent": "extractor",
    "input": pdf_path,
    "config": {...}
}

# Agent processes and returns
result = {
    "status": "success",
    "data": {...},
    "metrics": {...}
}
```

### Agent → Agent Handoff

```python
# Extractor passes to Validator
extracted_data = extractor.process(pdf)
validation_result = validator.process(extracted_data)

# Validator passes to Auditor
audit_result = auditor.process(validation_result)
```

## Performance Targets

| Agent | Target Time (per 100 pages) | Memory |
|-------|------------------------------|---------|
| Extractor | < 30 seconds | < 500MB |
| Validator | < 10 seconds | < 100MB |
| Auditor | < 20 seconds | < 200MB |
| QC Agent | < 5 seconds | < 50MB |

**Overall Target:** 600-page PDF processed in < 5 minutes with 99%+ accuracy

## Future Enhancements

- [ ] GPU acceleration for OCR
- [ ] Distributed processing for large documents
- [ ] Machine learning for pattern recognition
- [ ] Custom agent plugins
- [ ] Real-time processing dashboard
