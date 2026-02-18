#!/usr/bin/env python3
"""
Test script to demonstrate the multi-agent validation system.

This script loads the previously parsed CSV and runs it through the validation pipeline
to demonstrate the Validator, Auditor, and QC agents working together.
"""

import csv
import sys
from pathlib import Path
from loguru import logger
from src.agents.orchestrator import ValidationOrchestrator


def setup_logging():
    """Configure logging."""
    logger.remove()
    logger.add(sys.stdout, level="INFO")


def load_csv(csv_path: str):
    """Load codes from CSV file."""
    codes = []

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            codes.append({
                'division': row['Division'],
                'code': row['Code'],
                'title': row['Title']
            })

    logger.info(f"Loaded {len(codes)} codes from {csv_path}")
    return codes


def main():
    """Main test function."""
    setup_logging()

    logger.info("="*80)
    logger.info("Multi-Agent Validation System Test")
    logger.info("="*80)

    # Load the parsed CSV
    csv_path = "data/output/MasterFormat_2020 - pgs_17-39 - MasterFormat Groups, Subgroups, and Divisions_parsed.csv"

    if not Path(csv_path).exists():
        logger.error(f"CSV file not found: {csv_path}")
        logger.info("Please run the parser first with: python parse_csi.py <pdf_file>")
        return 1

    # Load codes
    codes = load_csv(csv_path)

    # Load configuration
    config_path = "config/validation_config.yaml"

    if Path(config_path).exists():
        logger.info(f"Loading configuration from: {config_path}")
        orchestrator = ValidationOrchestrator.load_config(config_path)
    else:
        logger.info("Using default configuration")
        orchestrator = ValidationOrchestrator()

    # Run validation
    logger.info(f"\nValidating {len(codes)} codes...")
    result = orchestrator.validate(
        codes,
        source_pdf=None,  # No PDF for spot-checking in this test
        export_report=True,
        report_path="data/output/validation_test_report.json"
    )

    # Display results
    logger.info("\n" + "="*80)
    logger.info("TEST RESULTS")
    logger.info("="*80)
    logger.info(f"Final Status: {result.status}")
    logger.info(f"Overall Confidence: {result.overall_confidence:.2f}%")
    logger.info(f"Requires Human Review: {result.requires_human_review}")
    logger.info("")
    logger.info("Issue Breakdown:")
    logger.info(f"  Total Issues: {result.total_issues}")
    logger.info(f"  - Critical: {result.critical_issues}")
    logger.info(f"  - High: {result.high_issues}")
    logger.info(f"  - Medium: {result.medium_issues}")
    logger.info(f"  - Low: {result.low_issues}")
    logger.info("")
    logger.info("Agent Results:")
    logger.info(f"  Validator: {'PASSED' if result.validator_result.passed else 'FAILED'} "
               f"({result.validator_result.confidence_score:.1f}% confidence)")
    logger.info(f"  Auditor: {'PASSED' if result.auditor_result.passed else 'FAILED'} "
               f"({len(result.auditor_result.issues)} issues, {len(result.auditor_result.anomalies)} anomalies)")
    logger.info(f"  QC: {'PASSED' if result.qc_result.passed else 'FAILED'} "
               f"({result.qc_result.overall_confidence:.1f}% confidence)")
    logger.info("")
    logger.info(f"Recommendation: {result.recommendation}")
    logger.info("="*80)

    # Show sample issues if any
    if result.issues_summary:
        logger.info("\nSample Issues (first 10):")
        for i, issue in enumerate(result.issues_summary[:10], 1):
            logger.info(f"  {i}. [{issue['severity']}] {issue['category']}: {issue['message']}")
            if issue.get('code'):
                logger.info(f"     Code: {issue['code']}")

    # Show low confidence entries if any
    if result.qc_result and result.qc_result.low_confidence_entries:
        logger.info(f"\nLow Confidence Entries: {len(result.qc_result.low_confidence_entries)}")
        for i, entry in enumerate(result.qc_result.low_confidence_entries[:5], 1):
            logger.info(f"  {i}. Line {entry['line_number']}: {entry['code']} - "
                       f"{entry['title'][:50]}... ({entry['confidence']:.2f} confidence)")
            logger.info(f"     Reasons: {', '.join(entry['reasons'])}")

    # Show edge cases if any
    if result.qc_result and result.qc_result.edge_cases:
        logger.info(f"\nEdge Cases Detected: {len(result.qc_result.edge_cases)}")
        edge_case_types = {}
        for ec in result.qc_result.edge_cases:
            edge_case_types[ec['type']] = edge_case_types.get(ec['type'], 0) + 1

        for ec_type, count in edge_case_types.items():
            logger.info(f"  - {ec_type}: {count}")

    logger.info("\nDetailed validation report saved to: data/output/validation_test_report.json")

    # Return exit code based on status
    if result.status == "PASS":
        logger.success("\n✓ Validation PASSED - Dataset is production-ready!")
        return 0
    elif result.status == "REVIEW":
        logger.warning("\n⚠ Validation requires REVIEW - Manual inspection recommended")
        return 1
    else:
        logger.error("\n✗ Validation FAILED - Critical issues must be fixed")
        return 2


if __name__ == "__main__":
    sys.exit(main())
