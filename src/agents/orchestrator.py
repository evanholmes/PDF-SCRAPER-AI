"""
Validation Orchestrator - Coordinates the multi-agent validation system.

This orchestrator manages the workflow of Validator, Auditor, and QC agents,
aggregates their results, and makes final quality decisions.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
from pathlib import Path
from loguru import logger

from src.agents.validator_agent import ValidatorAgent, ValidationResult
from src.agents.auditor_agent import AuditorAgent, AuditResult
from src.agents.qc_agent import QualityControlAgent, QCResult


@dataclass
class OrchestrationResult:
    """Final result from the orchestrated validation process."""
    status: str  # PASS, REVIEW, FAIL
    overall_confidence: float  # 0-100 scale
    requires_human_review: bool

    # Agent results
    validator_result: Optional[ValidationResult] = None
    auditor_result: Optional[AuditResult] = None
    qc_result: Optional[QCResult] = None

    # Aggregated data
    total_issues: int = 0
    critical_issues: int = 0
    high_issues: int = 0
    medium_issues: int = 0
    low_issues: int = 0

    issues_summary: List[Dict[str, Any]] = field(default_factory=list)
    recommendation: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary for JSON export."""
        return {
            'status': self.status,
            'overall_confidence': self.overall_confidence,
            'requires_human_review': self.requires_human_review,
            'total_issues': self.total_issues,
            'critical_issues': self.critical_issues,
            'high_issues': self.high_issues,
            'medium_issues': self.medium_issues,
            'low_issues': self.low_issues,
            'recommendation': self.recommendation,
            'timestamp': self.timestamp,
            'issues_summary': self.issues_summary
        }


class ValidationOrchestrator:
    """
    Orchestrates the multi-agent validation system.

    Workflow:
    1. Validator Agent: First-pass structural validation
    2. Auditor Agent: Logical verification and cross-referencing
    3. QC Agent: Final quality control and confidence scoring

    Quality Gates:
    - Critical Gate: Validator must pass with 0 critical errors
    - Warning Gate: Auditor warnings below threshold
    - Confidence Gate: QC confidence > threshold
    """

    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the Validation Orchestrator.

        Args:
            config: Configuration dictionary for all agents
        """
        self.config = config or {}

        # Initialize agents with their specific configs
        validator_config = self.config.get('validator', {})
        auditor_config = self.config.get('auditor', {})
        qc_config = self.config.get('qc', {})

        self.validator = ValidatorAgent(validator_config)
        self.auditor = AuditorAgent(auditor_config)
        self.qc = QualityControlAgent(qc_config)

        # Quality gate thresholds
        self.max_critical_errors = self.config.get('max_critical_errors', 0)
        self.max_high_issues = self.config.get('max_high_issues', 5)
        self.min_confidence = self.config.get('min_confidence', 95.0)

        logger.info("Validation Orchestrator initialized")

    def validate(self, codes: List[Dict[str, str]],
                source_pdf: str = None,
                export_report: bool = True,
                report_path: str = None) -> OrchestrationResult:
        """
        Run the complete multi-agent validation pipeline.

        Args:
            codes: List of parsed code dictionaries
            source_pdf: Optional path to source PDF for QC spot-checking
            export_report: Whether to export detailed report
            report_path: Path for report export (auto-generated if not provided)

        Returns:
            OrchestrationResult with complete validation assessment
        """
        logger.info("="*80)
        logger.info("Starting Multi-Agent Validation Pipeline")
        logger.info(f"Total codes to validate: {len(codes)}")
        logger.info("="*80)

        # Stage 1: Validator Agent
        logger.info("\n[STAGE 1/3] Running Validator Agent...")
        validator_result = self.validator.validate(codes)

        # Check critical gate
        critical_errors = [e for e in validator_result.errors if e.severity == 'CRITICAL']
        if len(critical_errors) > self.max_critical_errors:
            logger.error(f"CRITICAL GATE FAILED: {len(critical_errors)} critical errors (max: {self.max_critical_errors})")
            return self._create_failure_result(
                validator_result=validator_result,
                reason=f"Critical validation errors: {len(critical_errors)} found"
            )

        logger.info(f"✓ Validator passed with {validator_result.confidence_score:.1f}% confidence")

        # Stage 2: Auditor Agent
        logger.info("\n[STAGE 2/3] Running Auditor Agent...")
        auditor_result = self.auditor.audit(codes)

        # Check warning gate
        high_issues = [i for i in auditor_result.issues if i.severity == 'HIGH']
        if len(high_issues) > self.max_high_issues:
            logger.warning(f"WARNING GATE TRIGGERED: {len(high_issues)} high issues (threshold: {self.max_high_issues})")
            # Continue but flag for review

        logger.info(f"✓ Auditor completed with {len(auditor_result.issues)} issues, {len(auditor_result.anomalies)} anomalies")

        # Stage 3: QC Agent
        logger.info("\n[STAGE 3/3] Running Quality Control Agent...")
        qc_result = self.qc.verify(codes, source_pdf=source_pdf)

        # Check confidence gate
        if qc_result.overall_confidence < self.min_confidence:
            logger.warning(f"CONFIDENCE GATE: {qc_result.overall_confidence:.1f}% (threshold: {self.min_confidence}%)")

        logger.info(f"✓ QC completed with {qc_result.overall_confidence:.1f}% confidence")

        # Aggregate results
        logger.info("\n[AGGREGATION] Combining agent results...")
        result = self._aggregate_results(validator_result, auditor_result, qc_result)

        # Log final decision
        logger.info("="*80)
        logger.info(f"FINAL DECISION: {result.status}")
        logger.info(f"Overall Confidence: {result.overall_confidence:.1f}%")
        logger.info(f"Total Issues: {result.total_issues} (Critical: {result.critical_issues}, High: {result.high_issues})")
        logger.info(f"Human Review Required: {result.requires_human_review}")
        logger.info(f"Recommendation: {result.recommendation}")
        logger.info("="*80)

        # Export detailed report if requested
        if export_report:
            self._export_report(result, codes, report_path)

        return result

    def _aggregate_results(self, validator_result: ValidationResult,
                          auditor_result: AuditResult,
                          qc_result: QCResult) -> OrchestrationResult:
        """Aggregate results from all agents into final decision."""

        # Collect all issues
        all_issues = []

        # Add validator issues
        for error in validator_result.errors:
            all_issues.append({
                'agent': 'Validator',
                'severity': error.severity,
                'category': error.category,
                'message': error.message,
                'line_number': error.line_number,
                'code': error.code,
                'details': error.details
            })

        for warning in validator_result.warnings:
            all_issues.append({
                'agent': 'Validator',
                'severity': warning.severity,
                'category': warning.category,
                'message': warning.message,
                'line_number': warning.line_number,
                'code': warning.code,
                'details': warning.details
            })

        # Add auditor issues
        for issue in auditor_result.issues:
            all_issues.append({
                'agent': 'Auditor',
                'severity': issue.severity,
                'category': issue.category,
                'message': issue.message,
                'line_number': issue.line_number,
                'code': issue.code,
                'details': issue.details
            })

        # Add QC issues
        for issue in qc_result.issues:
            all_issues.append({
                'agent': 'QC',
                'severity': issue.severity,
                'category': issue.category,
                'message': issue.message,
                'line_number': issue.line_number,
                'code': issue.code,
                'details': issue.details if hasattr(issue, 'details') else {}
            })

        # Count issues by severity
        critical = sum(1 for i in all_issues if i['severity'] == 'CRITICAL')
        high = sum(1 for i in all_issues if i['severity'] == 'HIGH')
        medium = sum(1 for i in all_issues if i['severity'] == 'MEDIUM')
        low = sum(1 for i in all_issues if i['severity'] == 'LOW')

        # Calculate overall confidence (weighted average)
        validator_weight = 0.3
        auditor_weight = 0.3
        qc_weight = 0.4

        overall_confidence = (
            validator_result.confidence_score * validator_weight +
            (100 - len(auditor_result.issues) * 2) * auditor_weight +  # Rough scoring for auditor
            qc_result.overall_confidence * qc_weight
        )
        overall_confidence = max(0.0, min(100.0, overall_confidence))

        # Determine final status
        if critical > 0:
            status = "FAIL"
            requires_review = True
        elif high > self.max_high_issues or overall_confidence < self.min_confidence:
            status = "REVIEW"
            requires_review = True
        elif qc_result.requires_human_review:
            status = "REVIEW"
            requires_review = True
        else:
            status = "PASS"
            requires_review = False

        # Generate recommendation
        recommendation = self._generate_final_recommendation(
            status, overall_confidence, critical, high, medium,
            validator_result, auditor_result, qc_result
        )

        return OrchestrationResult(
            status=status,
            overall_confidence=overall_confidence,
            requires_human_review=requires_review,
            validator_result=validator_result,
            auditor_result=auditor_result,
            qc_result=qc_result,
            total_issues=len(all_issues),
            critical_issues=critical,
            high_issues=high,
            medium_issues=medium,
            low_issues=low,
            issues_summary=all_issues,
            recommendation=recommendation
        )

    def _create_failure_result(self, validator_result: ValidationResult = None,
                              auditor_result: AuditResult = None,
                              qc_result: QCResult = None,
                              reason: str = "") -> OrchestrationResult:
        """Create a failure result when a quality gate fails."""

        critical_count = 0
        if validator_result:
            critical_count = sum(1 for e in validator_result.errors if e.severity == 'CRITICAL')

        return OrchestrationResult(
            status="FAIL",
            overall_confidence=0.0,
            requires_human_review=True,
            validator_result=validator_result,
            auditor_result=auditor_result,
            qc_result=qc_result,
            total_issues=critical_count,
            critical_issues=critical_count,
            recommendation=f"FAILED: {reason}"
        )

    def _generate_final_recommendation(self, status: str, confidence: float,
                                      critical: int, high: int, medium: int,
                                      validator_result: ValidationResult,
                                      auditor_result: AuditResult,
                                      qc_result: QCResult) -> str:
        """Generate comprehensive final recommendation."""

        if status == "FAIL":
            return (f"Dataset FAILED validation with {critical} critical issues. "
                   f"Requires immediate correction before use.")

        if status == "REVIEW":
            reasons = []
            if high > self.max_high_issues:
                reasons.append(f"{high} high-priority issues")
            if confidence < self.min_confidence:
                reasons.append(f"confidence {confidence:.1f}% below threshold")
            if qc_result.requires_human_review:
                reasons.append("QC flagged for manual review")

            reason_str = ", ".join(reasons)
            return (f"Dataset requires REVIEW due to: {reason_str}. "
                   f"Recommend manual spot-check of {len(qc_result.low_confidence_entries)} "
                   f"low-confidence entries before production use.")

        # PASS status
        if confidence >= 98:
            return (f"Dataset PASSED with excellent quality ({confidence:.1f}% confidence). "
                   f"Ready for immediate production use with high confidence.")
        elif confidence >= 95:
            return (f"Dataset PASSED with good quality ({confidence:.1f}% confidence). "
                   f"Ready for production use. Minor issues detected but within acceptable limits.")
        else:
            return (f"Dataset PASSED with acceptable quality ({confidence:.1f}% confidence). "
                   f"Recommend periodic spot-checks during use.")

    def _export_report(self, result: OrchestrationResult,
                      codes: List[Dict[str, str]],
                      report_path: str = None) -> None:
        """Export detailed validation report to JSON."""

        if not report_path:
            # Auto-generate report path
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_path = f"data/output/validation_report_{timestamp}.json"

        # Create output directory if needed
        Path(report_path).parent.mkdir(parents=True, exist_ok=True)

        # Prepare detailed report
        report = {
            'summary': result.to_dict(),
            'validator': {
                'passed': result.validator_result.passed if result.validator_result else False,
                'confidence': result.validator_result.confidence_score if result.validator_result else 0,
                'stats': result.validator_result.stats if result.validator_result else {}
            },
            'auditor': {
                'passed': result.auditor_result.passed if result.auditor_result else False,
                'stats': result.auditor_result.stats if result.auditor_result else {},
                'anomaly_count': len(result.auditor_result.anomalies) if result.auditor_result else 0
            },
            'qc': {
                'confidence': result.qc_result.overall_confidence if result.qc_result else 0,
                'edge_cases': len(result.qc_result.edge_cases) if result.qc_result else 0,
                'low_confidence_entries': len(result.qc_result.low_confidence_entries) if result.qc_result else 0,
                'stats': result.qc_result.stats if result.qc_result else {}
            },
            'detailed_issues': result.issues_summary,
            'dataset_info': {
                'total_codes': len(codes),
                'divisions': len(set(c.get('division', '') for c in codes))
            }
        }

        # Write report
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)

        logger.info(f"Validation report exported to: {report_path}")

    @classmethod
    def load_config(cls, config_path: str) -> 'ValidationOrchestrator':
        """
        Load orchestrator configuration from YAML file.

        Args:
            config_path: Path to YAML configuration file

        Returns:
            Configured ValidationOrchestrator instance
        """
        import yaml

        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        return cls(config)
