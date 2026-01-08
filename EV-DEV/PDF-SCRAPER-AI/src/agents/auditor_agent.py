"""
Auditor Agent - Deep logical verification and cross-referencing.

This agent performs hierarchical analysis, sequence verification, and cross-reference
validation to ensure logical consistency and completeness of the parsed data.
"""

import re
from typing import List, Dict, Any, Set, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
from loguru import logger


@dataclass
class AuditIssue:
    """Represents a single audit issue."""
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    category: str  # Hierarchy, Sequence, CrossReference, Anomaly, Coverage
    message: str
    line_number: int = None
    code: str = None
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditResult:
    """Result of audit process."""
    passed: bool
    issues: List[AuditIssue] = field(default_factory=list)
    stats: Dict[str, Any] = field(default_factory=dict)
    anomalies: List[Dict[str, Any]] = field(default_factory=list)


class AuditorAgent:
    """
    Deep logical verification and cross-referencing agent.

    Responsibilities:
    - Hierarchical consistency (parent-child relationships)
    - Sequence verification (proper code ordering)
    - Cross-reference validation (against known structures)
    - Mathematical integrity
    - Contextual analysis (title appropriateness)
    - Anomaly detection
    - Coverage verification
    """

    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the Auditor Agent.

        Args:
            config: Configuration dictionary with audit rules
        """
        self.config = config or {}
        self.require_sequence_order = self.config.get('require_sequence_order', True)
        self.check_cross_references = self.config.get('check_cross_references', True)
        self.hierarchy_depth = self.config.get('hierarchy_depth', 3)
        self.detect_anomalies = self.config.get('detect_anomalies', True)

        # Known CSI MasterFormat divisions (for cross-reference)
        self.known_divisions = {
            '00': 'Procurement and Contracting Requirements',
            '01': 'General Requirements',
            '02': 'Existing Conditions',
            '03': 'Concrete',
            '04': 'Masonry',
            '05': 'Metals',
            '06': 'Wood, Plastics, and Composites',
            '07': 'Thermal and Moisture Protection',
            '08': 'Openings',
            '09': 'Finishes',
            '10': 'Specialties',
            '11': 'Equipment',
            '12': 'Furnishings',
            '13': 'Special Construction',
            '14': 'Conveying Equipment',
            '21': 'Fire Suppression',
            '22': 'Plumbing',
            '23': 'Heating, Ventilating, and Air Conditioning (HVAC)',
            '25': 'Integrated Automation',
            '26': 'Electrical',
            '27': 'Communications',
            '28': 'Electronic Safety and Security',
            '31': 'Earthwork',
            '32': 'Exterior Improvements',
            '33': 'Utilities',
            '34': 'Transportation',
            '35': 'Waterway and Marine Construction',
            '40': 'Process Integration',
            '41': 'Material Processing and Handling Equipment',
            '42': 'Process Heating, Cooling, and Drying Equipment',
            '43': 'Process Gas and Liquid Handling, Purification, and Storage Equipment',
            '44': 'Pollution and Waste Control Equipment',
            '45': 'Industry-Specific Manufacturing Equipment',
            '46': 'Water and Wastewater Equipment',
            '48': 'Electrical Power Generation'
        }

        logger.info("Auditor Agent initialized")

    def audit(self, codes: List[Dict[str, str]]) -> AuditResult:
        """
        Perform comprehensive audit on validated codes.

        Args:
            codes: List of parsed and validated code dictionaries

        Returns:
            AuditResult with issues, anomalies, and statistics
        """
        logger.info(f"Starting audit of {len(codes)} codes")

        issues = []
        anomalies = []

        # Track statistics
        stats = {
            'total_codes': len(codes),
            'divisions_found': 0,
            'hierarchy_levels': {},
            'sequence_breaks': 0,
            'unknown_divisions': 0,
            'anomalies_detected': 0
        }

        # Check for empty dataset
        if not codes:
            issues.append(AuditIssue(
                severity='CRITICAL',
                category='Coverage',
                message='No codes provided for audit'
            ))
            return AuditResult(passed=False, issues=issues, stats=stats)

        # Run audit checks
        issues.extend(self._check_hierarchical_consistency(codes, stats))
        issues.extend(self._verify_sequence_order(codes, stats))
        issues.extend(self._cross_reference_validation(codes, stats))
        issues.extend(self._analyze_context(codes))

        if self.detect_anomalies:
            anomalies = self._detect_anomalies(codes, stats)

        issues.extend(self._verify_coverage(codes, stats))

        # Determine pass/fail
        critical_issues = [i for i in issues if i.severity == 'CRITICAL']
        high_issues = [i for i in issues if i.severity == 'HIGH']

        passed = len(critical_issues) == 0 and len(high_issues) < 5  # Allow up to 5 high issues

        logger.info(
            f"Audit complete: {'PASSED' if passed else 'FAILED'} | "
            f"Issues: {len(issues)} | Anomalies: {len(anomalies)}"
        )

        return AuditResult(
            passed=passed,
            issues=issues,
            stats=stats,
            anomalies=anomalies
        )

    def _check_hierarchical_consistency(self, codes: List[Dict[str, str]],
                                       stats: Dict) -> List[AuditIssue]:
        """Verify parent-child code relationships and hierarchical structure."""
        issues = []

        # Build hierarchy map: division -> level1 -> level2
        hierarchy = defaultdict(lambda: defaultdict(set))

        for idx, code_entry in enumerate(codes, 1):
            division = code_entry.get('division', '')
            code = code_entry.get('code', '')

            # Parse code levels
            code_parts = re.sub(r'\s+', '', code).split()

            if len(code_parts) == 0:
                continue

            # For 4-digit codes: XX XX -> level 1
            # For 6-digit codes: XX XX XX -> level 2
            code_digits = ''.join(code_parts)

            if len(code_digits) == 4:
                level1 = code_digits[2:4]
                hierarchy[division][level1].add(None)
                stats['hierarchy_levels']['level1'] = stats['hierarchy_levels'].get('level1', 0) + 1
            elif len(code_digits) == 6:
                level1 = code_digits[2:4]
                level2 = code_digits[4:6]
                hierarchy[division][level1].add(level2)
                stats['hierarchy_levels']['level2'] = stats['hierarchy_levels'].get('level2', 0) + 1

        # Check for orphaned level 2 codes (level 2 without parent level 1)
        for division, level1_codes in hierarchy.items():
            for level1, level2_codes in level1_codes.items():
                # If we have level 2 codes but no None (indicating no level 1 parent)
                if level2_codes and None not in level2_codes and len(level2_codes) > 0:
                    # Check if parent level 1 exists
                    parent_code = f"{division} {level1}"
                    has_parent = any(
                        c.get('code', '').replace(' ', '')[:4] == f"{division}{level1}"
                        for c in codes
                    )

                    if not has_parent:
                        issues.append(AuditIssue(
                            severity='MEDIUM',
                            category='Hierarchy',
                            message=f'Level 2 codes found without parent level 1 code: Division {division}, Level {level1}',
                            code=parent_code,
                            details={'level2_codes': list(level2_codes)}
                        ))

        stats['divisions_found'] = len(hierarchy)

        return issues

    def _verify_sequence_order(self, codes: List[Dict[str, str]],
                               stats: Dict) -> List[AuditIssue]:
        """Verify that codes follow proper sequential ordering."""
        issues = []

        if not self.require_sequence_order:
            return issues

        prev_division = None
        prev_code_int = -1

        for idx, code_entry in enumerate(codes, 1):
            division = code_entry.get('division', '')
            code = code_entry.get('code', '')

            try:
                # Convert code to integer for comparison
                code_digits = re.sub(r'\s+', '', code)
                code_int = int(code_digits)
                division_int = int(division)

                # Check division sequence
                if prev_division is not None:
                    prev_div_int = int(prev_division)

                    # If division changed, it should increase
                    if division_int < prev_div_int:
                        issues.append(AuditIssue(
                            severity='HIGH',
                            category='Sequence',
                            message=f'Division sequence break: {prev_division} -> {division}',
                            line_number=idx,
                            code=code
                        ))
                        stats['sequence_breaks'] += 1

                # Check code sequence within division
                if division == prev_division:
                    # Within same division, codes should generally increase
                    # Allow some flexibility for hierarchical grouping
                    if code_int < prev_code_int - 10:  # Allow minor deviations
                        issues.append(AuditIssue(
                            severity='LOW',
                            category='Sequence',
                            message=f'Possible code sequence break in division {division}: {prev_code_int} -> {code_int}',
                            line_number=idx,
                            code=code
                        ))
                        stats['sequence_breaks'] += 1

                prev_division = division
                prev_code_int = code_int

            except (ValueError, AttributeError):
                issues.append(AuditIssue(
                    severity='MEDIUM',
                    category='Sequence',
                    message=f'Unable to verify sequence for code: {code}',
                    line_number=idx,
                    code=code
                ))

        return issues

    def _cross_reference_validation(self, codes: List[Dict[str, str]],
                                    stats: Dict) -> List[AuditIssue]:
        """Cross-reference codes against known CSI MasterFormat structure."""
        issues = []

        if not self.check_cross_references:
            return issues

        # Get unique divisions from parsed codes
        parsed_divisions = set(c.get('division', '') for c in codes)

        # Check for unknown divisions
        for division in parsed_divisions:
            if division and division not in self.known_divisions:
                issues.append(AuditIssue(
                    severity='MEDIUM',
                    category='CrossReference',
                    message=f'Unknown division found: {division} (not in CSI MasterFormat 2020)',
                    code=division,
                    details={'parsed_divisions': list(parsed_divisions)}
                ))
                stats['unknown_divisions'] += 1

        # Check for expected divisions that might be missing
        # (This is informational - not all documents contain all divisions)
        expected_common_divisions = {'00', '01', '02', '03', '04', '05'}
        missing_common = expected_common_divisions - parsed_divisions

        if missing_common and len(parsed_divisions) > 10:
            # Only flag if we have substantial content
            issues.append(AuditIssue(
                severity='LOW',
                category='Coverage',
                message=f'Some common divisions not found: {missing_common}',
                details={'note': 'This may be expected if document is a subset'}
            ))

        return issues

    def _analyze_context(self, codes: List[Dict[str, str]]) -> List[AuditIssue]:
        """Analyze whether titles make contextual sense for their codes."""
        issues = []

        # Define keywords that should typically appear in specific divisions
        division_keywords = {
            '03': ['concrete', 'cement', 'grout', 'reinforc', 'cast', 'precast'],
            '04': ['mason', 'brick', 'block', 'stone', 'mortar'],
            '05': ['metal', 'steel', 'aluminum', 'iron', 'structural'],
            '06': ['wood', 'plastic', 'composite', 'lumber', 'timber'],
            '07': ['thermal', 'insulation', 'moisture', 'roofing', 'waterproof'],
            '08': ['door', 'window', 'opening', 'glazing', 'entrance'],
            '09': ['finish', 'paint', 'coating', 'flooring', 'ceiling', 'wall'],
            '22': ['plumbing', 'pipe', 'water', 'drain', 'fixture'],
            '23': ['hvac', 'heating', 'cooling', 'ventilation', 'air'],
            '26': ['electrical', 'power', 'lighting', 'wiring', 'panel']
        }

        for idx, code_entry in enumerate(codes, 1):
            division = code_entry.get('division', '')
            title = code_entry.get('title', '').lower()
            code = code_entry.get('code', '')

            # Skip if not a division we have keywords for
            if division not in division_keywords:
                continue

            # Check if any expected keywords appear in title
            expected_keywords = division_keywords[division]
            has_keyword = any(keyword in title for keyword in expected_keywords)

            if not has_keyword and len(title) > 10:  # Only check substantive titles
                issues.append(AuditIssue(
                    severity='LOW',
                    category='Context',
                    message=f'Title may not match division context: Division {division} ({self.known_divisions.get(division, "Unknown")})',
                    line_number=idx,
                    code=code,
                    details={
                        'title': title,
                        'expected_keywords': expected_keywords
                    }
                ))

        return issues

    def _detect_anomalies(self, codes: List[Dict[str, str]],
                         stats: Dict) -> List[Dict[str, Any]]:
        """Detect unusual patterns or outliers in the data."""
        anomalies = []

        # Analyze title lengths
        title_lengths = [len(c.get('title', '')) for c in codes]
        avg_length = sum(title_lengths) / len(title_lengths) if title_lengths else 0

        # Detect unusually long or short titles
        for idx, code_entry in enumerate(codes, 1):
            title = code_entry.get('title', '')
            code = code_entry.get('code', '')

            if len(title) > avg_length * 3:  # 3x longer than average
                anomalies.append({
                    'type': 'unusually_long_title',
                    'line_number': idx,
                    'code': code,
                    'title': title,
                    'length': len(title),
                    'avg_length': avg_length
                })
                stats['anomalies_detected'] += 1
            elif len(title) < avg_length * 0.3 and len(title) > 0:  # 30% of average
                anomalies.append({
                    'type': 'unusually_short_title',
                    'line_number': idx,
                    'code': code,
                    'title': title,
                    'length': len(title),
                    'avg_length': avg_length
                })
                stats['anomalies_detected'] += 1

        # Detect gaps in code sequences
        codes_by_division = defaultdict(list)
        for code_entry in codes:
            division = code_entry.get('division', '')
            code = code_entry.get('code', '')
            try:
                code_int = int(re.sub(r'\s+', '', code))
                codes_by_division[division].append(code_int)
            except (ValueError, AttributeError):
                pass

        # Check for large gaps in sequences
        for division, code_list in codes_by_division.items():
            if len(code_list) < 2:
                continue

            sorted_codes = sorted(code_list)
            for i in range(len(sorted_codes) - 1):
                gap = sorted_codes[i + 1] - sorted_codes[i]
                if gap > 1000:  # Large gap detected
                    anomalies.append({
                        'type': 'large_sequence_gap',
                        'division': division,
                        'gap_size': gap,
                        'before_code': sorted_codes[i],
                        'after_code': sorted_codes[i + 1]
                    })
                    stats['anomalies_detected'] += 1

        logger.info(f"Detected {len(anomalies)} anomalies")
        return anomalies

    def _verify_coverage(self, codes: List[Dict[str, str]],
                        stats: Dict) -> List[AuditIssue]:
        """Verify that expected codes are present (coverage analysis)."""
        issues = []

        # Count codes per division
        codes_per_division = defaultdict(int)
        for code_entry in codes:
            division = code_entry.get('division', '')
            codes_per_division[division] += 1

        # Check for divisions with suspiciously few codes
        for division, count in codes_per_division.items():
            if count < 3 and division in self.known_divisions:
                issues.append(AuditIssue(
                    severity='LOW',
                    category='Coverage',
                    message=f'Division {division} has only {count} codes (may be incomplete)',
                    code=division,
                    details={'count': count}
                ))

        return issues
