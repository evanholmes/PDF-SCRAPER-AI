#!/usr/bin/env python3
"""
Main entry point for CSI MasterFormat PDF parsing with multi-agent validation.
"""
import argparse
import sys
import json
import csv
from pathlib import Path
from loguru import logger
from src.parsers.csi_parser_final import CSIParser
from src.models.csi_masterformat import CSICode
from src.agents.orchestrator import ValidationOrchestrator


def setup_logging(level: str = "INFO"):
    """Configure logging."""
    logger.remove()
    logger.add(sys.stdout, level=level)


def parse_pdf(pdf_path: str, output_path: str = None, format: str = "csv",
              validate: bool = True, config_path: str = None):
    """Parse CSI MasterFormat PDF and export results with optional multi-agent validation."""
    logger.info(f"Starting parse of: {pdf_path}")

    # Initialize parser
    parser = CSIParser(column_split_x=320.0)

    # Parse PDF
    raw_codes = parser.parse_pdf(pdf_path)

    # Convert to Pydantic models for basic validation
    validated_codes = []
    errors = []

    for raw_code in raw_codes:
        try:
            code = CSICode(
                division=raw_code['division'],
                code=raw_code['code'],
                title=raw_code['title'],
                group=raw_code.get('group'),
                subgroup=raw_code.get('subgroup'),
                page_number=raw_code.get('page_number')
            )
            validated_codes.append(code)
        except Exception as e:
            errors.append(f"Validation error for {raw_code}: {e}")
            logger.warning(f"Skipping invalid code: {e}")

    logger.info(f"Validated {len(validated_codes)} codes ({len(errors)} errors)")

    # Run multi-agent validation if requested
    validation_result = None
    if validate:
        logger.info("\n" + "="*80)
        logger.info("Running Multi-Agent Validation System")
        logger.info("="*80)

        # Load configuration
        if config_path:
            orchestrator = ValidationOrchestrator.load_config(config_path)
        else:
            # Use default config
            default_config_path = Path(__file__).parent / "config" / "validation_config.yaml"
            if default_config_path.exists():
                orchestrator = ValidationOrchestrator.load_config(str(default_config_path))
            else:
                orchestrator = ValidationOrchestrator()

        # Convert validated codes back to dicts for agent processing
        codes_as_dicts = [
            {
                'division': c.division,
                'code': c.code,
                'title': c.title
            }
            for c in validated_codes
        ]

        # Run validation pipeline
        validation_result = orchestrator.validate(
            codes_as_dicts,
            source_pdf=pdf_path,
            export_report=True
        )

        # Log validation summary
        logger.info("\n" + "="*80)
        logger.info("VALIDATION SUMMARY")
        logger.info("="*80)
        logger.info(f"Status: {validation_result.status}")
        logger.info(f"Confidence: {validation_result.overall_confidence:.1f}%")
        logger.info(f"Total Issues: {validation_result.total_issues}")
        logger.info(f"  - Critical: {validation_result.critical_issues}")
        logger.info(f"  - High: {validation_result.high_issues}")
        logger.info(f"  - Medium: {validation_result.medium_issues}")
        logger.info(f"  - Low: {validation_result.low_issues}")
        logger.info(f"Requires Review: {validation_result.requires_human_review}")
        logger.info(f"Recommendation: {validation_result.recommendation}")
        logger.info("="*80 + "\n")

        # Stop export if validation failed critically
        if validation_result.status == "FAIL":
            logger.error("Validation FAILED - export cancelled. Fix critical issues and retry.")
            return validated_codes, errors, validation_result

    # Determine output path
    if not output_path:
        pdf_name = Path(pdf_path).stem
        output_path = f"data/output/{pdf_name}_parsed.{format}"

    # Export
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if format == "csv":
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Division", "Code", "Title", "Group", "Subgroup", "Page"])
            for code in validated_codes:
                writer.writerow([
                    code.division,
                    code.code,
                    code.title,
                    code.group or '',
                    code.subgroup or '',
                    code.page_number or ''
                ])
    elif format == "json":
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump([code.dict() for code in validated_codes], f, indent=2)

    logger.success(f"Exported {len(validated_codes)} codes to: {output_path}")

    return validated_codes, errors, validation_result


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Parse CSI MasterFormat PDFs with multi-agent validation"
    )
    parser.add_argument("input", help="Input PDF file path")
    parser.add_argument("-o", "--output", help="Output file path (default: auto-generated)")
    parser.add_argument("-f", "--format", choices=["csv", "json"], default="csv",
                       help="Output format")
    parser.add_argument("--no-validate", action="store_true",
                       help="Skip multi-agent validation (faster but less thorough)")
    parser.add_argument("-c", "--config", help="Path to validation config YAML file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose logging")

    args = parser.parse_args()

    # Setup logging
    log_level = "DEBUG" if args.verbose else "INFO"
    setup_logging(log_level)

    # Parse and export
    try:
        codes, errors, validation_result = parse_pdf(
            args.input,
            args.output,
            args.format,
            validate=not args.no_validate,
            config_path=args.config
        )

        if errors:
            logger.warning(f"Completed with {len(errors)} validation errors")
            for error in errors[:10]:
                logger.warning(error)

        # Return appropriate exit code based on validation
        if validation_result:
            if validation_result.status == "FAIL":
                return 2  # Critical failure
            elif validation_result.status == "REVIEW":
                return 1  # Requires review

        return 0  # Success
    except Exception as e:
        logger.error(f"Parsing failed: {e}")
        import traceback
        logger.debug(traceback.format_exc())
        return 1


if __name__ == "__main__":
    sys.exit(main())
