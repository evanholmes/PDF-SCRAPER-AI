"""
BID-AI Integrated Bid Classifier
Combines keyword matching + equipment capability verification
THE BID MASTER's decision engine for opportunity classification
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

from loguru import logger
from sqlalchemy.orm import Session

from ..database.models import Opportunity
from .capability_matcher import (
    CapabilityMatch,
    CapabilityMatcher,
    CapabilityPhase,
    get_capability_matcher,
)
from .keyword_matcher import KeywordMatcher, MatchResult


@dataclass
class BidClassification:
    """Complete bid classification result"""

    # Final Decision
    final_tier: str  # A, B, C, D, E
    final_rationale: str
    can_fulfill: bool
    should_bid: bool

    # Scoring
    relevance_score: int  # 0-100 from keyword matching
    capability_confidence: float  # 0-100 from capability matching
    overall_score: float  # Combined weighted score

    # Keyword Analysis
    keywords_matched: List[str]
    keyword_tier: str
    keyword_rationale: str

    # Capability Analysis
    equipment_matched: List[str]
    capabilities_matched: List[str]
    materials_matched: List[str]
    capability_phase: CapabilityPhase
    capability_tier: str
    capability_rationale: str

    # Recommendations
    action_required: str  # 'BID', 'REVIEW', 'ASSIGN', 'PARTNER', 'ARCHIVE'
    notes: List[str]

    def to_dict(self) -> Dict:
        """Convert to dictionary for database storage"""
        return {
            "tier": self.final_tier,
            "tier_rationale": self.final_rationale,
            "relevance_score": self.relevance_score,
            "keywords_matched": self.keywords_matched,
            "equipment_matched": self.equipment_matched,
            "can_fulfill": self.can_fulfill,
            "action_required": self.action_required,
            "notes": self.notes,
        }


class BidClassifier:
    """
    THE BID MASTER's classification engine
    Integrates keyword relevance + equipment capabilities for intelligent tier assignment
    """

    def __init__(self, session: Session):
        """
        Initialize classifier with database session

        Args:
            session: SQLAlchemy session for keyword lookup
        """
        self.keyword_matcher = KeywordMatcher(session)
        self.capability_matcher = get_capability_matcher()
        self.session = session
        logger.info("BidClassifier initialized with keyword and capability matchers")

    def classify(
        self,
        title: str,
        description: str = "",
        category: str = "",
        estimated_value: float = None,
    ) -> BidClassification:
        """
        Classify an opportunity with full analysis

        Args:
            title: Opportunity title
            description: Opportunity description
            category: Opportunity category/type
            estimated_value: Estimated contract value (optional)

        Returns:
            Complete BidClassification
        """
        # Step 1: Keyword matching (industry relevance)
        keyword_result = self.keyword_matcher.match_opportunity(
            title=title, description=description, category=category
        )

        # Step 2: Capability matching (can we fulfill?)
        capability_result = self.capability_matcher.match_opportunity(
            title=title,
            description=description,
            keywords_matched=keyword_result.keywords_matched,
        )

        # Step 3: Combine results for final classification
        final_tier, final_rationale, action = self._determine_final_tier(
            keyword_result, capability_result, estimated_value
        )

        # Step 4: Calculate overall score
        overall_score = self._calculate_overall_score(
            keyword_result.relevance_score, capability_result.confidence
        )

        # Step 5: Determine if we should bid
        should_bid = self._should_bid(final_tier, capability_result, estimated_value)

        # Compile notes
        notes = []
        if capability_result.notes:
            notes.extend(capability_result.notes)
        if estimated_value and estimated_value > 100000:
            notes.append(f"High-value opportunity: ${estimated_value:,.2f}")
        if capability_result.phase == CapabilityPhase.PHASE_2:
            notes.append(
                "Requires Phase 2 capabilities (CNC Millwork) - not active yet"
            )

        return BidClassification(
            # Final Decision
            final_tier=final_tier,
            final_rationale=final_rationale,
            can_fulfill=capability_result.can_fulfill,
            should_bid=should_bid,
            # Scoring
            relevance_score=keyword_result.relevance_score,
            capability_confidence=capability_result.confidence,
            overall_score=overall_score,
            # Keyword Analysis
            keywords_matched=keyword_result.keywords_matched,
            keyword_tier=keyword_result.tier_suggestion,
            keyword_rationale=keyword_result.tier_rationale,
            # Capability Analysis
            equipment_matched=capability_result.equipment_matched,
            capabilities_matched=capability_result.capabilities_matched,
            materials_matched=capability_result.materials_matched,
            capability_phase=capability_result.phase,
            capability_tier=capability_result.recommended_tier,
            capability_rationale=capability_result.tier_rationale,
            # Recommendations
            action_required=action,
            notes=notes,
        )

    def _determine_final_tier(
        self,
        keyword_result: MatchResult,
        capability_result: CapabilityMatch,
        estimated_value: float = None,
    ) -> tuple:
        """
        Determine final tier based on both keyword and capability analysis

        Returns: (tier, rationale, action)
        """
        kr = keyword_result
        cr = capability_result

        # TIER A: High relevance + Can fulfill with current equipment
        if (
            kr.relevance_score >= 30
            and cr.can_fulfill
            and cr.phase == CapabilityPhase.CURRENT
        ):
            return (
                "A",
                f"DIRECT FULFILLMENT: {kr.relevance_score}% relevance, equipment verified ({', '.join(cr.equipment_matched[:2])})",
                "BID",
            )

        # TIER A (lower confidence): Moderate relevance + Can fulfill
        if (
            kr.relevance_score >= 20
            and cr.can_fulfill
            and cr.phase == CapabilityPhase.CURRENT
        ):
            return (
                "A",
                f"FULFILL (Review): {kr.relevance_score}% relevance, equipment matched - verify scope",
                "REVIEW",
            )

        # TIER B: Relevant but Phase 2 capability needed
        if (
            kr.relevance_score >= 20
            and cr.can_fulfill
            and cr.phase == CapabilityPhase.PHASE_2
        ):
            return (
                "B",
                f"PHASE 2 CAPABILITY: Millwork opportunity - assign to partner or defer",
                "ASSIGN",
            )

        # TIER B: Relevant industry, but can't fulfill (assignment opportunity)
        if kr.relevance_score >= 20 and not cr.can_fulfill:
            return (
                "B",
                f"ASSIGNMENT: {kr.relevance_score}% relevance, no equipment match - find partner",
                "ASSIGN",
            )

        # TIER C: Partner network required
        if cr.phase == CapabilityPhase.PARTNER and kr.relevance_score >= 10:
            return (
                "C",
                f"PARTNER REQUIRED: Capability exists via partner network",
                "PARTNER",
            )

        # TIER C: Partial capability match, needs partnership
        if kr.relevance_score >= 10 and cr.confidence > 0 and not cr.can_fulfill:
            return (
                "C",
                f"PARTNERSHIP: Partial match ({kr.relevance_score}%) - joint bid opportunity",
                "PARTNER",
            )

        # TIER D: Low relevance but adjacent industry
        if kr.relevance_score >= 5:
            return (
                "D",
                f"BROKER: Low relevance ({kr.relevance_score}%) - consulting/bid-writing opportunity",
                "REVIEW",
            )

        # TIER E: Not relevant
        return (
            "E",
            f"ARCHIVE: No relevance ({kr.relevance_score}%), no capability match",
            "ARCHIVE",
        )

    def _calculate_overall_score(
        self, relevance_score: int, capability_confidence: float
    ) -> float:
        """
        Calculate combined overall score
        Weighted: 60% relevance, 40% capability
        """
        return (relevance_score * 0.6) + (capability_confidence * 0.4)

    def _should_bid(
        self,
        tier: str,
        capability_result: CapabilityMatch,
        estimated_value: float = None,
    ) -> bool:
        """Determine if we should actively pursue this bid"""

        # Tier A: Always consider bidding
        if tier == "A":
            return True

        # Tier B with high-value: Consider for referral fee
        if tier == "B" and estimated_value and estimated_value > 50000:
            return True

        # Other tiers: Don't actively pursue
        return False

    def classify_opportunity(self, opportunity: Opportunity) -> BidClassification:
        """
        Classify an existing Opportunity object

        Args:
            opportunity: Opportunity model instance

        Returns:
            BidClassification
        """
        return self.classify(
            title=opportunity.title,
            description=opportunity.description or "",
            category=opportunity.category or "",
            estimated_value=float(opportunity.estimated_value)
            if opportunity.estimated_value
            else None,
        )

    def update_opportunity_classification(
        self, opportunity: Opportunity
    ) -> BidClassification:
        """
        Classify and update an opportunity in the database

        Args:
            opportunity: Opportunity to classify and update

        Returns:
            BidClassification result
        """
        result = self.classify_opportunity(opportunity)

        # Update the opportunity
        opportunity.tier = result.final_tier
        opportunity.tier_rationale = result.final_rationale
        opportunity.relevance_score = result.relevance_score
        opportunity.keywords_matched = result.keywords_matched

        self.session.add(opportunity)

        logger.info(
            f"Classified opportunity {opportunity.id}: "
            f"Tier {result.final_tier} ({result.action_required})"
        )

        return result

    def bulk_classify(
        self, opportunities: List[Opportunity]
    ) -> Dict[int, BidClassification]:
        """
        Classify multiple opportunities

        Args:
            opportunities: List of Opportunity objects

        Returns:
            Dict mapping opportunity ID to classification
        """
        results = {}

        for opp in opportunities:
            results[opp.id] = self.classify_opportunity(opp)

        # Summary stats
        tier_counts = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0}
        for classification in results.values():
            tier_counts[classification.final_tier] += 1

        logger.info(
            f"Bulk classified {len(opportunities)} opportunities: {tier_counts}"
        )

        return results


def quick_classify(
    title: str, description: str = "", session: Session = None
) -> BidClassification:
    """
    Quick classification without instantiating BidClassifier

    Args:
        title: Opportunity title
        description: Opportunity description
        session: Database session (required)

    Returns:
        BidClassification
    """
    if session is None:
        raise ValueError("Database session is required")

    classifier = BidClassifier(session)
    return classifier.classify(title, description)


if __name__ == "__main__":
    # Test the integrated classifier
    from ..config.settings import get_settings
    from ..database.connection import get_session, init_db

    settings = get_settings()
    init_db(settings.database.url)

    print("=" * 70)
    print("BID-AI INTEGRATED CLASSIFIER TEST")
    print("THE BID MASTER's Decision Engine")
    print("=" * 70)

    with get_session() as session:
        classifier = BidClassifier(session)

        test_opportunities = [
            {
                "title": "RFP for Wayfinding Signage System - City Hall",
                "description": "Design, fabrication and installation of interior wayfinding signage including dimensional letters, directional signs, and ADA-compliant room identification in acrylic.",
                "value": 75000,
            },
            {
                "title": "Large Format Printing and Vehicle Wrap Services",
                "description": "Provide large format vinyl graphics, vehicle wraps, and banner printing for municipal fleet.",
                "value": 45000,
            },
            {
                "title": "Illuminated Channel Letter Signage",
                "description": "Fabricate and install LED illuminated channel letters for new recreation center building identification.",
                "value": 120000,
            },
            {
                "title": "Custom CNC Millwork for Library Renovation",
                "description": "Architectural millwork including custom cabinetry, decorative panels, and wood moldings.",
                "value": 200000,
            },
            {
                "title": "Traffic Sign Replacement Program",
                "description": "Supply traffic signs, parking signs, and reflective directional signage.",
                "value": 35000,
            },
            {
                "title": "Road Paving and Asphalt Services",
                "description": "Asphalt paving and road maintenance for municipal roads and parking lots.",
                "value": 500000,
            },
        ]

        print("\n")
        for i, opp in enumerate(test_opportunities, 1):
            result = classifier.classify(
                title=opp["title"],
                description=opp["description"],
                estimated_value=opp.get("value"),
            )

            print(f"{'=' * 70}")
            print(f"📋 TEST {i}: {opp['title'][:50]}...")
            print(f"{'=' * 70}")
            print(f"💰 Estimated Value: ${opp.get('value', 0):,.0f}")
            print()
            print(f"🎯 FINAL TIER: {result.final_tier}")
            print(f"📊 Overall Score: {result.overall_score:.1f}%")
            print(
                f"   Relevance: {result.relevance_score}% | Capability: {result.capability_confidence}%"
            )
            print()
            print(f"✅ Can Fulfill: {'YES' if result.can_fulfill else 'NO'}")
            print(f"🚀 Should Bid: {'YES' if result.should_bid else 'NO'}")
            print(f"📌 Action: {result.action_required}")
            print()
            print(f"📝 Rationale: {result.final_rationale}")

            if result.equipment_matched:
                print(f"🔧 Equipment: {', '.join(result.equipment_matched[:3])}")
            if result.keywords_matched:
                print(f"🔑 Keywords: {', '.join(result.keywords_matched[:5])}")
            if result.materials_matched:
                print(f"🧱 Materials: {', '.join(list(result.materials_matched)[:3])}")
            if result.notes:
                print(f"📝 Notes:")
                for note in result.notes:
                    print(f"   • {note}")
            print()

        print("=" * 70)
        print("✅ BID CLASSIFIER TEST COMPLETE")
        print("=" * 70)
