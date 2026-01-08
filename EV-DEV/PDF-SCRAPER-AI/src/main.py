#!/usr/bin/env python3
"""
Main entry point for CSI MasterFormat PDF parsing.
"""
import argparse
import sys
import json
import csv
from pathlib import Path
from loguru import logger
from src.parsers.csi_parser_final import CSIParser
from src.models.csi_masterformat import CSICode, ParsingResult


def setup_logging(level: str = "INFO"):
    """Configure logging."""
    logger.remove()
    logger.add(sys.stdout, level=level)


def parse_pdf(pdf_path: str, output_path: str = None, format: str = "csv"):
    """Parse CSI MasterFormat PDF and export results."""
    logger.info(f"Starting parse of: {pdf_path}")
    
    # Initialize parser
    parser = CSIParser(column_split_x=320.0)
    
    # Parse PDF
    raw_codes = parser.parse_pdf(pdf_path)
    
    # Convert to Pydantic models for validation
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
    
    return validated_codes, errors


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Parse CSI MasterFormat PDFs")
    parser.add_argument("input", help="Input PDF file path")
    parser.add_argument("-o", "--output", help="Output file path (default: auto-generated)")
    parser.add_argument("-f", "--format", choices=["csv", "json"], default="csv", help="Output format")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose logging")
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = "DEBUG" if args.verbose else "INFO"
    setup_logging(log_level)
    
    # Parse and export
    try:
        codes, errors = parse_pdf(args.input, args.output, args.format)
        
        if errors:
            logger.warning(f"Completed with {len(errors)} validation errors")
            for error in errors[:10]:  # Show first 10 errors
                logger.warning(error)
        
        return 0
    except Exception as e:
        logger.error(f"Parsing failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
