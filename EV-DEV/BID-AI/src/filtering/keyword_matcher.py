"""
Keyword matching and relevance scoring for bid opportunities
THE BID MASTER uses this to identify signage and printing contracts
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from loguru import logger
from sqlalchemy.orm import Session

from ..database.models import Keyword, Opportunity


@dataclass
class MatchResult:
    """Result of keyword matching"""

    keywords_matched: List[str]
    relevance_score: int
    match_details: Dict[str, int]  # keyword -> count
    tier_suggestion: str
    tier_rationale: str


class KeywordMatcher:
    """
    Intelligent keyword matching for opportunity filtering
    """

    def __init__(self, session: Session):
        """
        Initialize matcher with database session

        Args:
            session: SQLAlchemy session
        """
        self.session = session
        self._load_keywords()

    def _load_keywords(self):
        """Load active keywords from database"""
        keywords = self.session.query(Keyword).filter(Keyword.is_active == True).all()

        # Organize by category for quick lookup
        self.keywords_by_category = {}
        self.all_keywords = {}

        for kw in keywords:
            # Store by category
            if kw.category not in self.keywords_by_category:
                self.keywords_by_category[kw.category] = []
            self.keywords_by_category[kw.category].append(kw)

            # Store all
            self.all_keywords[kw.keyword.lower()] = kw

        logger.info(
            f"Loaded {len(keywords)} active keywords across {len(self.keywords_by_category)} categories"
        )

    def match_opportunity(
        self, title: str, description: str = "", category: str = ""
    ) -> MatchResult:
        """
        Match keywords against an opportunity

        Args:
            title: Opportunity title
            description: Opportunity description
            category: Opportunity category/type

        Returns:
            MatchResult with matched keywords and relevance score
        """
        title_lower = title.lower()
        description_lower = description.lower() if description else ""
        category_lower = category.lower() if category else ""

        matched_keywords = []
        match_details = {}
        total_score = 0

        # Search for each keyword
        for keyword, kw_obj in self.all_keywords.items():
            count = 0

            # Check title (weighted higher)
            title_count = title_lower.count(keyword)
            if title_count > 0:
                count += title_count
                total_score += kw_obj.weight * title_count * 2  # Title matches worth 2x

            # Check description
            desc_count = description_lower.count(keyword)
            if desc_count > 0:
                count += desc_count
                total_score += kw_obj.weight * desc_count

            # Check category
            if keyword in category_lower:
                count += 1
                total_score += kw_obj.weight * 3  # Category matches worth 3x

            if count > 0:
                matched_keywords.append(keyword)
                match_details[keyword] = count

        # Cap score at 100
        relevance_score = min(total_score, 100)

        # Determine tier suggestion
        tier, rationale = self._suggest_tier(
            matched_keywords, relevance_score, match_details
        )

        return MatchResult(
            keywords_matched=matched_keywords,
            relevance_score=relevance_score,
            match_details=match_details,
            tier_suggestion=tier,
            tier_rationale=rationale,
        )

    def _suggest_tier(
        self,
        matched_keywords: List[str],
        relevance_score: int,
        match_details: Dict[str, int],
    ) -> Tuple[str, str]:
        """
        Suggest tier classification based on matches

        Returns:
            Tuple of (tier, rationale)
        """
        if relevance_score == 0:
            return "E", "No relevant keywords matched - Archive"

        # Check for our core capabilities
        signage_keywords = [
            "signage",
            "wayfinding",
            "sign",
            "dimensional letters",
            "monument sign",
            "pylon sign",
            "channel letters",
        ]
        printing_keywords = [
            "printing",
            "print",
            "large format",
            "digital printing",
            "banners",
            "vinyl graphics",
        ]
        cnc_keywords = ["cnc", "millwork", "router"]

        signage_matches = [k for k in matched_keywords if k in signage_keywords]
        printing_matches = [k for k in matched_keywords if k in printing_keywords]
        cnc_matches = [k for k in matched_keywords if k in cnc_keywords]

        # Tier A: We can definitely fulfill this
        if (
            signage_matches or printing_matches or cnc_matches
        ) and relevance_score >= 30:
            capabilities = []
            if signage_matches:
                capabilities.append("signage")
            if printing_matches:
                capabilities.append("printing")
            if cnc_matches:
                capabilities.append("CNC/millwork")

            return (
                "A",
                f"Direct fulfillment - Matches our {'/'.join(capabilities)} capabilities (score: {relevance_score})",
            )

        # Tier B: Relevant but outside our direct capabilities - potential assignment
        elif relevance_score >= 20:
            return (
                "B",
                f"Assignment opportunity - Relevant to industry but may need partner (score: {relevance_score})",
            )

        # Tier C: Partial match - potential partnership
        elif relevance_score >= 10:
            return (
                "C",
                f"Partnership potential - Partial capability match (score: {relevance_score})",
            )

        # Tier D: Low relevance - brokering opportunity
        elif relevance_score >= 5:
            return (
                "D",
                f"Brokering opportunity - Low relevance but industry-adjacent (score: {relevance_score})",
            )

        # Tier E: Archive
        else:
            return "E", f"Archive - Minimal relevance (score: {relevance_score})"

    def bulk_match_opportunities(
        self, opportunities: List[Opportunity]
    ) -> Dict[int, MatchResult]:
        """
        Match multiple opportunities at once

        Args:
            opportunities: List of Opportunity objects

        Returns:
            Dict mapping opportunity ID to MatchResult
        """
        results = {}

        for opp in opportunities:
            result = self.match_opportunity(
                title=opp.title,
                description=opp.description or "",
                category=opp.category or "",
            )
            results[opp.id] = result

        logger.info(f"Matched {len(opportunities)} opportunities")
        return results

    def update_opportunity_matching(self, opportunity: Opportunity) -> MatchResult:
        """
        Match and update an opportunity in the database

        Args:
            opportunity: Opportunity object to match and update

        Returns:
            MatchResult
        """
        result = self.match_opportunity(
            title=opportunity.title,
            description=opportunity.description or "",
            category=opportunity.category or "",
        )

        # Update opportunity
        opportunity.keywords_matched = result.keywords_matched
        opportunity.relevance_score = result.relevance_score
        opportunity.tier = result.tier_suggestion
        opportunity.tier_rationale = result.tier_rationale

        self.session.add(opportunity)

        logger.debug(
            f"Opportunity {opportunity.id} matched: "
            f"Tier {result.tier_suggestion}, Score {result.relevance_score}"
        )

        return result

    def get_category_stats(self, matched_keywords: List[str]) -> Dict[str, int]:
        """
        Get statistics about which categories were matched

        Args:
            matched_keywords: List of matched keyword strings

        Returns:
            Dict of category -> count
        """
        category_counts = {}

        for kw_str in matched_keywords:
            kw_obj = self.all_keywords.get(kw_str.lower())
            if kw_obj and kw_obj.category:
                category_counts[kw_obj.category] = (
                    category_counts.get(kw_obj.category, 0) + 1
                )

        return category_counts


# Convenience function for quick matching
def quick_match(
    title: str, description: str = "", session: Session = None
) -> MatchResult:
    """
    Quick keyword matching without needing to instantiate KeywordMatcher

    Args:
        title: Opportunity title
        description: Opportunity description
        session: Database session (required)

    Returns:
        MatchResult
    """
    if session is None:
        raise ValueError("Database session is required")

    matcher = KeywordMatcher(session)
    return matcher.match_opportunity(title, description)


if __name__ == "__main__":
    # Example usage / testing
    from ..database.connection import get_session

    with get_session() as session:
        matcher = KeywordMatcher(session)

        # Test case 1: High relevance signage opportunity
        result1 = matcher.match_opportunity(
            title="RFP for Wayfinding Signage System - City Hall",
            description="Design, fabrication and installation of interior and exterior wayfinding signage including monument signs, directional signs, and ADA-compliant room identification signs.",
        )
        print(f"\nTest 1: Signage RFP")
        print(f"  Matched: {result1.keywords_matched}")
        print(f"  Score: {result1.relevance_score}")
        print(f"  Tier: {result1.tier_suggestion}")
        print(f"  Rationale: {result1.tier_rationale}")

        # Test case 2: Printing opportunity
        result2 = matcher.match_opportunity(
            title="Large Format Printing Services",
            description="Provide large format digital printing for banners, posters, and vehicle wraps",
        )
        print(f"\nTest 2: Printing Services")
        print(f"  Matched: {result2.keywords_matched}")
        print(f"  Score: {result2.relevance_score}")
        print(f"  Tier: {result2.tier_suggestion}")

        # Test case 3: Irrelevant opportunity
        result3 = matcher.match_opportunity(
            title="RFP for Road Paving Services",
            description="Asphalt paving and road maintenance",
        )
        print(f"\nTest 3: Road Paving (Irrelevant)")
        print(f"  Matched: {result3.keywords_matched}")
        print(f"  Score: {result3.relevance_score}")
        print(f"  Tier: {result3.tier_suggestion}")
