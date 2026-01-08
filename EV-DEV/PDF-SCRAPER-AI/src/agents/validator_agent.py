"""
Validator Agent - First-pass validation for structural integrity and format compliance.

This agent performs schema validation, format checking, and basic integrity verification
to ensure the parsed data meets fundamental quality standards.
"""

import re
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass, field
from loguru import logger


@dataclass
class ValidationError:
    """Represents a single validation error."""
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    category: str  # Schema, Format, Integrity, Duplicate, etc.
    message: str
    line_number: int = None
    code: str = None
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationResult:
    """Result of validation process."""
    passed: bool
    confidence_score: float  # 0-100
    errors: List[ValidationError] = field(default_factory=list)
    warnings: List[ValidationError] = field(default_factory=list)
    stats: Dict[str, Any] = field(default_factory=dict)


class ValidatorAgent:
    """
    First-pass validator ensuring structural integrity and format compliance.

    Responsibilities:
    - Schema validation (correct columns, data types)
    - Code format validation (XX XX or XX XX XX)
    - Division-code consistency
    - Title completeness
    - Required field presence
    - Character encoding integrity
    - Duplicate detection
    """

    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the Validator Agent.

        Args:
            config: Configuration dictionary with validation rules
        """
        self.config = config or {}
        self.strict_mode = self.config.get('strict_mode', True)
        self.allow_4_digit_codes = self.config.get('allow_4_digit_codes', True)
        self.allow_6_digit_codes = self.config.get('allow_6_digit_codes', True)
        self.max_title_length = self.config.get('max_title_length', 200)
        self.min_title_length = self.config.get('min_title_length', 2)

        # Patterns
        self.code_4_digit_pattern = re.compile(r'^\d{2}\s+\d{2}$')
        self.code_6_digit_pattern = re.compile(r'^\d{2}\s+\d{2}\s+\d{2}$')
        self.division_pattern = re.compile(r'^\d{2}$')

        logger.info("Validator Agent initialized")

    def validate(self, codes: List[Dict[str, str]]) -> ValidationResult:
        """
        Perform comprehensive validation on parsed codes.

        Args:
            codes: List of parsed code dictionaries with 'division', 'code', 'title' keys

        Returns:
            ValidationResult with errors, warnings, and confidence score
        """
        logger.info(f"Starting validation of {len(codes)} codes")

        errors = []
        warnings = []

        # Track statistics
        stats = {
            'total_codes': len(codes),
            'codes_4_digit': 0,
            'codes_6_digit': 0,
            'duplicates_found': 0,
            'encoding_issues': 0
        }

        # Check for empty dataset
        if not codes:
            errors.append(ValidationError(
                severity='CRITICAL',
                category='Schema',
                message='No codes provided for validation'
            ))
            return ValidationResult(passed=False, confidence_score=0.0, errors=errors, stats=stats)

        # Run validation checks
        errors.extend(self._validate_schema(codes))
        errors.extend(self._validate_format(codes, stats))
        errors.extend(self._validate_division_consistency(codes))
        errors.extend(self._validate_completeness(codes))
        warnings.extend(self._validate_encoding(codes, stats))
        errors.extend(self._detect_duplicates(codes, stats))

        # Calculate confidence score
        critical_errors = [e for e in errors if e.severity == 'CRITICAL']
        high_errors = [e for e in errors if e.severity == 'HIGH']
        medium_errors = [e for e in errors if e.severity == 'MEDIUM']

        confidence_score = self._calculate_confidence(
            total=len(codes),
            critical=len(critical_errors),
            high=len(high_errors),
            medium=len(medium_errors),
            warnings=len(warnings)
        )

        # Determine pass/fail
        passed = len(critical_errors) == 0 and len(high_errors) == 0

        logger.info(
            f"Validation complete: {'PASSED' if passed else 'FAILED'} | "
            f"Confidence: {confidence_score:.1f}% | "
            f"Errors: {len(errors)} | Warnings: {len(warnings)}"
        )

        return ValidationResult(
            passed=passed,
            confidence_score=confidence_score,
            errors=errors,
            warnings=warnings,
            stats=stats
        )

    def _validate_schema(self, codes: List[Dict[str, str]]) -> List[ValidationError]:
        """Validate that all required fields are present with correct types."""
        errors = []
        required_fields = {'division', 'code', 'title'}

        for idx, code_entry in enumerate(codes, 1):
            # Check for required fields
            missing_fields = required_fields - set(code_entry.keys())
            if missing_fields:
                errors.append(ValidationError(
                    severity='CRITICAL',
                    category='Schema',
                    message=f'Missing required fields: {missing_fields}',
                    line_number=idx,
                    code=code_entry.get('code', 'UNKNOWN')
                ))

            # Check that all fields are strings
            for field, value in code_entry.items():
                if not isinstance(value, str):
                    errors.append(ValidationError(
                        severity='HIGH',
                        category='Schema',
                        message=f'Field "{field}" must be string, got {type(value).__name__}',
                        line_number=idx,
                        code=code_entry.get('code', 'UNKNOWN')
                    ))

        return errors

    def _validate_format(self, codes: List[Dict[str, str]], stats: Dict) -> List[ValidationError]:
        """Validate code and division format compliance."""
        errors = []

        for idx, code_entry in enumerate(codes, 1):
            division = code_entry.get('division', '')
            code = code_entry.get('code', '')

            # Validate division format (2 digits)
            if not self.division_pattern.match(division):
                errors.append(ValidationError(
                    severity='CRITICAL',
                    category='Format',
                    message=f'Invalid division format: "{division}" (must be 2 digits)',
                    line_number=idx,
                    code=code
                ))

            # Validate code format (4 or 6 digits with spaces)
            is_4_digit = self.code_4_digit_pattern.match(code)
            is_6_digit = self.code_6_digit_pattern.match(code)

            if is_4_digit and not self.allow_4_digit_codes:
                errors.append(ValidationError(
                    severity='HIGH',
                    category='Format',
                    message=f'4-digit codes not allowed in strict mode: "{code}"',
                    line_number=idx,
                    code=code
                ))
            elif is_6_digit and not self.allow_6_digit_codes:
                errors.append(ValidationError(
                    severity='HIGH',
                    category='Format',
                    message=f'6-digit codes not allowed: "{code}"',
                    line_number=idx,
                    code=code
                ))
            elif not (is_4_digit or is_6_digit):
                errors.append(ValidationError(
                    severity='CRITICAL',
                    category='Format',
                    message=f'Invalid code format: "{code}" (must be XX XX or XX XX XX)',
                    line_number=idx,
                    code=code
                ))

            # Track statistics
            if is_4_digit:
                stats['codes_4_digit'] += 1
            elif is_6_digit:
                stats['codes_6_digit'] += 1

        return errors

    def _validate_division_consistency(self, codes: List[Dict[str, str]]) -> List[ValidationError]:
        """Ensure code's first two digits match its division."""
        errors = []

        for idx, code_entry in enumerate(codes, 1):
            division = code_entry.get('division', '')
            code = code_entry.get('code', '')

            if not division or not code:
                continue

            # Extract first two digits from code
            code_digits = re.sub(r'\s+', '', code)  # Remove spaces
            if len(code_digits) >= 2:
                code_prefix = code_digits[:2]

                if code_prefix != division:
                    errors.append(ValidationError(
                        severity='HIGH',
                        category='Consistency',
                        message=f'Division "{division}" does not match code prefix "{code_prefix}" in code "{code}"',
                        line_number=idx,
                        code=code
                    ))

        return errors

    def _validate_completeness(self, codes: List[Dict[str, str]]) -> List[ValidationError]:
        """Validate that titles are complete (no truncation, proper length)."""
        errors = []

        for idx, code_entry in enumerate(codes, 1):
            title = code_entry.get('title', '')
            code = code_entry.get('code', '')

            # Check for empty title
            if not title or not title.strip():
                errors.append(ValidationError(
                    severity='CRITICAL',
                    category='Completeness',
                    message='Title is empty',
                    line_number=idx,
                    code=code
                ))
                continue

            # Check for suspiciously short titles
            if len(title.strip()) < self.min_title_length:
                errors.append(ValidationError(
                    severity='HIGH',
                    category='Completeness',
                    message=f'Title suspiciously short: "{title}" ({len(title)} chars)',
                    line_number=idx,
                    code=code
                ))

            # Check for suspiciously long titles (possible merge error)
            if len(title) > self.max_title_length:
                errors.append(ValidationError(
                    severity='MEDIUM',
                    category='Completeness',
                    message=f'Title suspiciously long: {len(title)} chars (max: {self.max_title_length})',
                    line_number=idx,
                    code=code,
                    details={'title_preview': title[:100] + '...'}
                ))

            # Check for incomplete title indicators
            truncation_indicators = ['...', '…', '..', 'Procuremen', 'Constructio']
            for indicator in truncation_indicators:
                if indicator in title:
                    errors.append(ValidationError(
                        severity='HIGH',
                        category='Completeness',
                        message=f'Possible title truncation detected: "{indicator}" in "{title}"',
                        line_number=idx,
                        code=code
                    ))
                    break

        return errors

    def _validate_encoding(self, codes: List[Dict[str, str]], stats: Dict) -> List[ValidationError]:
        """Check for character encoding issues."""
        warnings = []

        # Common encoding error indicators
        bad_chars = ['�', '\ufffd', '\x00']

        for idx, code_entry in enumerate(codes, 1):
            title = code_entry.get('title', '')
            code = code_entry.get('code', '')

            for bad_char in bad_chars:
                if bad_char in title:
                    warnings.append(ValidationError(
                        severity='MEDIUM',
                        category='Encoding',
                        message=f'Possible encoding issue detected: "{bad_char}" in title',
                        line_number=idx,
                        code=code,
                        details={'title': title}
                    ))
                    stats['encoding_issues'] += 1
                    break

        return warnings

    def _detect_duplicates(self, codes: List[Dict[str, str]], stats: Dict) -> List[ValidationError]:
        """Detect duplicate code entries."""
        errors = []
        seen_codes = {}

        for idx, code_entry in enumerate(codes, 1):
            division = code_entry.get('division', '')
            code = code_entry.get('code', '')
            full_code = f"{division}-{code}"

            if full_code in seen_codes:
                errors.append(ValidationError(
                    severity='HIGH',
                    category='Duplicate',
                    message=f'Duplicate code detected: {full_code}',
                    line_number=idx,
                    code=code,
                    details={
                        'first_occurrence': seen_codes[full_code],
                        'duplicate_occurrence': idx
                    }
                ))
                stats['duplicates_found'] += 1
            else:
                seen_codes[full_code] = idx

        return errors

    def _calculate_confidence(self, total: int, critical: int, high: int,
                            medium: int, warnings: int) -> float:
        """
        Calculate confidence score based on error distribution.

        Formula:
        - Critical errors: -50 points each
        - High errors: -10 points each
        - Medium errors: -2 points each
        - Warnings: -0.5 points each
        - Base score: 100%
        """
        score = 100.0

        # Deduct points for errors
        score -= (critical * 50)
        score -= (high * 10)
        score -= (medium * 2)
        score -= (warnings * 0.5)

        # Ensure score stays within 0-100 range
        score = max(0.0, min(100.0, score))

        return score
