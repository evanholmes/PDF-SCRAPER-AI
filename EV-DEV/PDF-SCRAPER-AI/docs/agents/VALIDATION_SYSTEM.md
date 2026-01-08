# Multi-Agent Validation System

## Overview
The validation system employs three specialized agents coordinated by an Orchestrator to ensure zero-error parsing of dense PDFs. Each agent has a specific responsibility and works in sequence to provide comprehensive quality assurance.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      ORCHESTRATOR                            │
│  - Coordinates agent workflow                                │
│  - Aggregates results                                        │
│  - Makes final quality decision                              │
└─────────────────────────────────────────────────────────────┘
                          │
         ┌────────────────┼────────────────┐
         ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  VALIDATOR   │  │   AUDITOR    │  │  QC AGENT    │
│   AGENT      │  │    AGENT     │  │              │
└──────────────┘  └──────────────┘  └──────────────┘
```

## Agent Responsibilities

### 1. Validator Agent
**Role**: First-pass validation ensuring structural integrity and format compliance

**Checks**:
- Schema validation (correct columns, data types)
- Code format validation (XX XX or XX XX XX)
- Division-code consistency (code matches its division)
- Title completeness (no truncation, no multi-line breaks)
- Required field presence (no missing data)
- Character encoding integrity (no garbled text)
- Duplicate detection (same code appears multiple times)

**Output**:
- List of validation errors with line numbers
- Confidence score (0-100%)
- Pass/fail status for each category

### 2. Auditor Agent
**Role**: Deep logical verification and cross-referencing

**Checks**:
- Hierarchical consistency (parent-child code relationships)
- Sequence verification (codes follow proper ordering)
- Cross-reference validation against known CSI MasterFormat structure
- Mathematical integrity (code calculations, if applicable)
- Contextual analysis (title makes sense for code)
- Anomaly detection (outliers, unusual patterns)
- Coverage verification (all expected codes present)

**Output**:
- List of logical inconsistencies with severity levels
- Cross-reference mismatches
- Missing expected codes
- Anomaly report with explanations

### 3. Quality Control Agent
**Role**: Final verification with human-like judgment and edge case detection

**Checks**:
- Edge case detection (boundary conditions, rare patterns)
- Ambiguity resolution (unclear title/code mappings)
- Confidence scoring for each parsed entry
- Sample spot-checking against original PDF
- Formatting consistency across entire dataset
- Final completeness verification
- Human-readability assessment

**Output**:
- Overall quality score (0-100%)
- List of low-confidence entries requiring human review
- Edge cases found with recommendations
- Final pass/fail recommendation

## Orchestrator Logic

### Workflow
1. **Validator Agent** runs first
   - If fails with critical errors: STOP, report issues
   - If passes: continue to Auditor

2. **Auditor Agent** runs second
   - If finds logical inconsistencies: flag for review
   - If passes: continue to QC

3. **QC Agent** runs third
   - Performs final verification
   - Assigns overall confidence score
   - Makes final recommendation

### Quality Gates
- **Critical Gate**: Validator must pass with 0 critical errors
- **Warning Gate**: Auditor warnings below threshold (configurable)
- **Confidence Gate**: QC confidence score > 95% for auto-approval

### Aggregation
```python
final_decision = {
    "status": "PASS" | "REVIEW" | "FAIL",
    "validator_results": {...},
    "auditor_results": {...},
    "qc_results": {...},
    "overall_confidence": 0-100,
    "requires_human_review": bool,
    "issues_summary": [...]
}
```

## Error Severity Levels

### CRITICAL (Auto-fail)
- Invalid code format
- Missing required fields
- Data corruption
- Structural integrity failure

### HIGH (Requires review)
- Logical inconsistencies
- Missing expected codes
- Hierarchical violations
- Anomalies with unclear cause

### MEDIUM (Warning)
- Formatting inconsistencies
- Low confidence scores
- Edge cases
- Unusual patterns

### LOW (Informational)
- Style deviations
- Minor formatting differences
- Suggestions for improvement

## Performance Targets

- **Validation Speed**: < 1 second per 1000 codes
- **Accuracy**: 99.9%+ detection of errors
- **False Positives**: < 1%
- **Memory Usage**: < 500MB for 10,000 codes
- **Parallel Processing**: Support for multi-threading

## Configuration

Each agent is configurable via YAML:

```yaml
validator:
  strict_mode: true
  allow_4_digit_codes: true
  allow_6_digit_codes: true
  max_title_length: 200
  
auditor:
  require_sequence_order: true
  check_cross_references: true
  hierarchy_depth: 3
  
qc:
  confidence_threshold: 0.95
  sample_size: 100
  spot_check_percentage: 5
```

## Integration with Parser

```python
from src.agents.orchestrator import ValidationOrchestrator
from src.parsers.csi_parser_final import CSIParser

# Parse PDF
parser = CSIParser()
codes = parser.parse_pdf("document.pdf")

# Validate with multi-agent system
orchestrator = ValidationOrchestrator()
result = orchestrator.validate(codes, source_pdf="document.pdf")

if result["status"] == "PASS":
    # Export validated data
    export_to_csv(codes, "output.csv")
elif result["status"] == "REVIEW":
    # Flag for human review
    send_for_review(codes, result["issues_summary"])
else:
    # Critical failure
    raise ValidationError(result["issues_summary"])
```

## Future Enhancements

1. **Machine Learning Integration**
   - Train models on validated datasets
   - Improve anomaly detection
   - Auto-suggest corrections

2. **Real-time Validation**
   - Stream validation during parsing
   - Early error detection
   - Faster feedback loops

3. **Custom Rule Engine**
   - User-defined validation rules
   - Domain-specific checks
   - Extensible plugin system

4. **Visualization Dashboard**
   - Real-time validation status
   - Error distribution charts
   - Confidence score trends
