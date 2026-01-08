"""
Quality Control Agent - Final verification with human-like judgment.

This agent performs edge case detection, confidence scoring, and final quality
assessment with human-like reasoning to catch anything the other agents missed.
"""

import re
import random
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass, field
from collections import Counter
from loguru import logger


@dataclass
class QCIssue:
    """Represents a quality control concern."""
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    category: str  # EdgeCase, Confidence, Formatting, Readability
    message: str
    line_number: int = None
    code: str = None
    confidence: float = None  # 0-1 scale
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class QCResult:
    """Result of quality control process."""
    passed: bool
    overall_confidence: float  # 0-100 scale
    requires_human_review: bool
    issues: List[QCIssue] = field(default_factory=list)
    low_confidence_entries: List[Dict[str, Any]] = field(default_factory=list)
    edge_cases: List[Dict[str, Any]] = field(default_factory=list)
    stats: Dict[str, Any] = field(default_factory=dict)
    recommendation: str = ""


class QualityControlAgent:
    """
    Final verification agent with human-like judgment and edge case detection.

    Responsibilities:
    - Edge case detection (boundary conditions, rare patterns)
    - Ambiguity resolution
    - Confidence scoring for each entry
    - Sample spot-checking
    - Formatting consistency
    - Final completeness verification
    - Human-readability assessment
    - Final pass/fail recommendation
    """

    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the Quality Control Agent.

        Args:
            config: Configuration dictionary with QC parameters
        """
        self.config = config or {}
        self.confidence_threshold = self.config.get('confidence_threshold', 0.95)
        self.sample_size = self.config.get('sample_size', 100)
        self.spot_check_percentage = self.config.get('spot_check_percentage', 5)

        logger.info("Quality Control Agent initialized")

    def verify(self, codes: List[Dict[str, str]],
              source_pdf: str = None) -> QCResult:
        """
        Perform final quality control verification.

        Args:
            codes: List of parsed and validated code dictionaries
            source_pdf: Optional path to source PDF for spot-checking

        Returns:
            QCResult with final assessment and recommendations
        """
        logger.info(f"Starting QC verification of {len(codes)} codes")

        issues = []
        low_confidence_entries = []
        edge_cases = []

        # Track statistics
        stats = {
            'total_codes': len(codes),
            'edge_cases_found': 0,
            'low_confidence_count': 0,
            'formatting_issues': 0,
            'avg_confidence': 0.0
        }

        # Check for empty dataset
        if not codes:
            return QCResult(
                passed=False,
                overall_confidence=0.0,
                requires_human_review=True,
                recommendation="FAIL: No codes provided for QC verification",
                stats=stats
            )

        # Run QC checks
        issues.extend(self._detect_edge_cases(codes, edge_cases, stats))
        issues.extend(self._check_formatting_consistency(codes, stats))
        issues.extend(self._assess_readability(codes))

        # Calculate confidence scores
        confidence_results = self._calculate_confidence_scores(codes, stats)
        low_confidence_entries = confidence_results['low_confidence']
        stats['avg_confidence'] = confidence_results['avg_confidence']
        stats['low_confidence_count'] = len(low_confidence_entries)

        # Perform spot check if source PDF provided
        if source_pdf:
            issues.extend(self._spot_check_sample(codes, source_pdf, stats))

        # Final completeness check
        issues.extend(self._verify_final_completeness(codes))

        # Calculate overall confidence and make recommendation
        overall_confidence = self._calculate_overall_confidence(
            codes, issues, stats, confidence_results
        )

        requires_review = overall_confidence < (self.confidence_threshold * 100)

        # Generate recommendation
        recommendation = self._generate_recommendation(
            overall_confidence, issues, stats, requires_review
        )

        # Determine pass/fail
        critical_issues = [i for i in issues if i.severity == 'CRITICAL']
        passed = (
            len(critical_issues) == 0 and
            overall_confidence >= (self.confidence_threshold * 100) and
            not requires_review
        )

        logger.info(
            f"QC verification complete: {'PASSED' if passed else 'REQUIRES REVIEW'} | "
            f"Confidence: {overall_confidence:.1f}% | "
            f"Issues: {len(issues)} | Low confidence: {len(low_confidence_entries)}"
        )

        return QCResult(
            passed=passed,
            overall_confidence=overall_confidence,
            requires_human_review=requires_review,
            issues=issues,
            low_confidence_entries=low_confidence_entries,
            edge_cases=edge_cases,
            stats=stats,
            recommendation=recommendation
        )

    def _detect_edge_cases(self, codes: List[Dict[str, str]],
                          edge_cases: List[Dict], stats: Dict) -> List[QCIssue]:
        """Detect edge cases and boundary conditions."""
        issues = []

        for idx, code_entry in enumerate(codes, 1):
            division = code_entry.get('division', '')
            code = code_entry.get('code', '')
            title = code_entry.get('title', '')

            # Edge case: Codes ending in 00 (typically high-level categories)
            if code.strip().endswith('00'):
                edge_cases.append({
                    'type': 'category_code',
                    'line_number': idx,
                    'code': code,
                    'title': title,
                    'note': 'High-level category code (ends in 00)'
                })
                stats['edge_cases_found'] += 1

            # Edge case: Very short codes (potentially incomplete)
            code_digits = re.sub(r'\s+', '', code)
            if len(code_digits) < 4:
                issues.append(QCIssue(
                    severity='MEDIUM',
                    category='EdgeCase',
                    message=f'Unusually short code: "{code}" ({len(code_digits)} digits)',
                    line_number=idx,
                    code=code,
                    confidence=0.7
                ))
                edge_cases.append({
                    'type': 'short_code',
                    'line_number': idx,
                    'code': code,
                    'title': title
                })
                stats['edge_cases_found'] += 1

            # Edge case: Titles with special characters
            special_char_pattern = re.compile(r'[^\w\s\-,().&/]')
            if special_char_pattern.search(title):
                edge_cases.append({
                    'type': 'special_characters',
                    'line_number': idx,
                    'code': code,
                    'title': title,
                    'characters': special_char_pattern.findall(title)
                })
                stats['edge_cases_found'] += 1

            # Edge case: Titles with numbers (potentially reference codes)
            if re.search(r'\d{3,}', title):  # 3+ consecutive digits
                edge_cases.append({
                    'type': 'numeric_content',
                    'line_number': idx,
                    'code': code,
                    'title': title,
                    'note': 'Title contains numeric sequences'
                })
                stats['edge_cases_found'] += 1

            # Edge case: All caps titles (might be section headers)
            if title.isupper() and len(title) > 5:
                edge_cases.append({
                    'type': 'all_caps',
                    'line_number': idx,
                    'code': code,
                    'title': title,
                    'note': 'All caps title (possibly section header)'
                })
                stats['edge_cases_found'] += 1

            # Edge case: Repeated words in title
            words = title.lower().split()
            word_counts = Counter(words)
            repeated = [word for word, count in word_counts.items() if count > 1 and len(word) > 3]
            if repeated:
                edge_cases.append({
                    'type': 'repeated_words',
                    'line_number': idx,
                    'code': code,
                    'title': title,
                    'repeated_words': repeated
                })
                stats['edge_cases_found'] += 1

        logger.info(f"Detected {len(edge_cases)} edge cases")
        return issues

    def _check_formatting_consistency(self, codes: List[Dict[str, str]],
                                     stats: Dict) -> List[QCIssue]:
        """Check for formatting consistency across the dataset."""
        issues = []

        # Check title case consistency
        title_cases = {
            'title_case': 0,
            'sentence_case': 0,
            'lower_case': 0,
            'upper_case': 0,
            'mixed': 0
        }

        for idx, code_entry in enumerate(codes, 1):
            title = code_entry.get('title', '')
            code = code_entry.get('code', '')

            if not title:
                continue

            # Classify title case
            if title.istitle():
                title_cases['title_case'] += 1
            elif title.isupper():
                title_cases['upper_case'] += 1
            elif title.islower():
                title_cases['lower_case'] += 1
            elif title[0].isupper() and not title.istitle():
                title_cases['sentence_case'] += 1
            else:
                title_cases['mixed'] += 1

        # Check if formatting is inconsistent
        dominant_case = max(title_cases, key=title_cases.get)
        dominant_count = title_cases[dominant_case]
        total = sum(title_cases.values())

        if total > 0:
            consistency_ratio = dominant_count / total

            if consistency_ratio < 0.8:  # Less than 80% consistent
                issues.append(QCIssue(
                    severity='LOW',
                    category='Formatting',
                    message=f'Inconsistent title case formatting: {dominant_case} ({consistency_ratio:.1%} consistent)',
                    details={'case_distribution': title_cases}
                ))
                stats['formatting_issues'] += 1

        # Check spacing consistency in codes
        spacing_patterns = Counter()
        for code_entry in codes:
            code = code_entry.get('code', '')
            spacing_patterns[code.count(' ')] += 1

        if len(spacing_patterns) > 2:  # Multiple spacing patterns
            issues.append(QCIssue(
                severity='LOW',
                category='Formatting',
                message=f'Inconsistent code spacing patterns detected',
                details={'spacing_distribution': dict(spacing_patterns)}
            ))
            stats['formatting_issues'] += 1

        return issues

    def _assess_readability(self, codes: List[Dict[str, str]]) -> List[QCIssue]:
        """Assess human readability of titles."""
        issues = []

        # Common readability issues
        readability_problems = [
            (r'[A-Z]{10,}', 'Excessive consecutive capitals'),
            (r'\s{2,}', 'Multiple consecutive spaces'),
            (r'([^\s])\1{4,}', 'Repeated characters'),
            (r'^[^A-Za-z]', 'Title starts with non-letter'),
        ]

        for idx, code_entry in enumerate(codes, 1):
            title = code_entry.get('title', '')
            code = code_entry.get('code', '')

            for pattern, problem_desc in readability_problems:
                if re.search(pattern, title):
                    issues.append(QCIssue(
                        severity='LOW',
                        category='Readability',
                        message=f'{problem_desc} in title',
                        line_number=idx,
                        code=code,
                        details={'title': title}
                    ))

        return issues

    def _calculate_confidence_scores(self, codes: List[Dict[str, str]],
                                     stats: Dict) -> Dict[str, Any]:
        """Calculate confidence score for each code entry."""
        low_confidence = []
        confidence_scores = []

        # Calculate average title length for comparison
        title_lengths = [len(c.get('title', '')) for c in codes]
        avg_title_length = sum(title_lengths) / len(title_lengths) if title_lengths else 0

        for idx, code_entry in enumerate(codes, 1):
            division = code_entry.get('division', '')
            code = code_entry.get('code', '')
            title = code_entry.get('title', '')

            confidence = 1.0  # Start with perfect confidence
            reasons = []

            # Reduce confidence for various issues

            # Title length anomalies
            if len(title) < avg_title_length * 0.3:
                confidence -= 0.2
                reasons.append('Title significantly shorter than average')
            elif len(title) > avg_title_length * 3:
                confidence -= 0.1
                reasons.append('Title significantly longer than average')

            # Code format issues
            code_digits = re.sub(r'\s+', '', code)
            if len(code_digits) < 4:
                confidence -= 0.3
                reasons.append('Code appears incomplete')

            # Special characters or unusual patterns
            if re.search(r'[^\w\s\-,().&/]', title):
                confidence -= 0.1
                reasons.append('Special characters in title')

            # Ending with punctuation (might be incomplete)
            if title.strip().endswith(('-', '—', ',')):
                confidence -= 0.2
                reasons.append('Title ends with punctuation')

            # Single letter or very short words
            words = title.split()
            if words and sum(1 for w in words if len(w) <= 1) > len(words) * 0.3:
                confidence -= 0.15
                reasons.append('Many single-letter words')

            # Missing title
            if not title.strip():
                confidence = 0.0
                reasons.append('Missing title')

            # Ensure confidence stays in valid range
            confidence = max(0.0, min(1.0, confidence))
            confidence_scores.append(confidence)

            # Track low confidence entries
            if confidence < self.confidence_threshold:
                low_confidence.append({
                    'line_number': idx,
                    'code': code,
                    'division': division,
                    'title': title,
                    'confidence': confidence,
                    'reasons': reasons
                })

        avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0

        return {
            'avg_confidence': avg_confidence * 100,  # Convert to percentage
            'low_confidence': low_confidence,
            'confidence_scores': confidence_scores
        }

    def _spot_check_sample(self, codes: List[Dict[str, str]],
                          source_pdf: str, stats: Dict) -> List[QCIssue]:
        """Perform spot-check sampling against source PDF."""
        issues = []

        # Calculate sample size
        total_codes = len(codes)
        sample_size = min(
            self.sample_size,
            max(int(total_codes * (self.spot_check_percentage / 100)), 5)
        )

        # Random sampling
        if total_codes > sample_size:
            sample_indices = random.sample(range(total_codes), sample_size)
        else:
            sample_indices = range(total_codes)

        logger.info(f"Spot-checking {len(sample_indices)} random samples")

        # Note: Actual PDF comparison would require PDF parsing
        # For now, log that spot-check is needed
        issues.append(QCIssue(
            severity='LOW',
            category='SpotCheck',
            message=f'Manual spot-check recommended for {len(sample_indices)} samples',
            details={
                'sample_count': len(sample_indices),
                'sample_indices': list(sample_indices)[:10]  # Show first 10
            }
        ))

        return issues

    def _verify_final_completeness(self, codes: List[Dict[str, str]]) -> List[QCIssue]:
        """Final completeness verification."""
        issues = []

        # Check for completely empty entries
        empty_count = 0
        for idx, code_entry in enumerate(codes, 1):
            if not any(code_entry.values()):
                issues.append(QCIssue(
                    severity='CRITICAL',
                    category='Completeness',
                    message='Completely empty entry found',
                    line_number=idx
                ))
                empty_count += 1

        # Check for minimum dataset size
        if len(codes) < 10:
            issues.append(QCIssue(
                severity='MEDIUM',
                category='Completeness',
                message=f'Very small dataset: only {len(codes)} codes (expected more)',
                details={'code_count': len(codes)}
            ))

        return issues

    def _calculate_overall_confidence(self, codes: List[Dict[str, str]],
                                     issues: List[QCIssue], stats: Dict,
                                     confidence_results: Dict) -> float:
        """Calculate overall confidence score for the entire dataset."""
        base_confidence = confidence_results['avg_confidence']

        # Deduct points for issues
        critical_count = sum(1 for i in issues if i.severity == 'CRITICAL')
        high_count = sum(1 for i in issues if i.severity == 'HIGH')
        medium_count = sum(1 for i in issues if i.severity == 'MEDIUM')

        deductions = (critical_count * 20) + (high_count * 5) + (medium_count * 2)

        overall = base_confidence - deductions
        overall = max(0.0, min(100.0, overall))

        return overall

    def _generate_recommendation(self, confidence: float, issues: List[QCIssue],
                                stats: Dict, requires_review: bool) -> str:
        """Generate final recommendation message."""
        critical = sum(1 for i in issues if i.severity == 'CRITICAL')
        high = sum(1 for i in issues if i.severity == 'HIGH')

        if critical > 0:
            return f"FAIL: {critical} critical issues found. Dataset requires correction before use."

        if confidence >= 98:
            return f"PASS: Excellent quality ({confidence:.1f}% confidence). Dataset ready for production use."
        elif confidence >= 95:
            return f"PASS: Good quality ({confidence:.1f}% confidence). Dataset ready for use with minor monitoring."
        elif confidence >= 90:
            return f"REVIEW: Acceptable quality ({confidence:.1f}% confidence). Recommend spot-check before production use."
        else:
            return f"REVIEW: Below threshold ({confidence:.1f}% confidence). Manual review required before use."
