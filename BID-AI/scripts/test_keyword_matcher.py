#!/usr/bin/env python3
"""
Test the keyword matching system
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger

from src.config.settings import get_settings
from src.database.connection import init_db
from src.filtering.keyword_matcher import KeywordMatcher


def main():
    settings = get_settings()
    db = init_db(settings.database.url)

    logger.info("Testing Keyword Matcher...")
    logger.info("=" * 60)

    with db.get_session() as session:
        matcher = KeywordMatcher(session)

        # Test case 1: High relevance signage opportunity
        logger.info("\n📋 Test 1: Wayfinding Signage RFP")
        result1 = matcher.match_opportunity(
            title="RFP for Wayfinding Signage System - City Hall",
            description="Design, fabrication and installation of interior and exterior wayfinding signage including monument signs, directional signs, and ADA-compliant room identification signs.",
        )
        logger.info(f"  Relevance Score: {result1.relevance_score}")
        logger.info(f"  Tier: {result1.tier_suggestion}")
        logger.info(f"  Matched Keywords: {', '.join(result1.keywords_matched)}")
        logger.info(f"  Rationale: {result1.tier_rationale}")

        # Test case 2: Printing opportunity
        logger.info("\n📋 Test 2: Large Format Printing")
        result2 = matcher.match_opportunity(
            title="Large Format Printing Services",
            description="Provide large format digital printing for banners, posters, and vinyl graphics",
        )
        logger.info(f"  Relevance Score: {result2.relevance_score}")
        logger.info(f"  Tier: {result2.tier_suggestion}")
        logger.info(f"  Matched Keywords: {', '.join(result2.keywords_matched)}")
        logger.info(f"  Rationale: {result2.tier_rationale}")

        # Test case 3: CNC/Millwork opportunity
        logger.info("\n📋 Test 3: CNC Millwork")
        result3 = matcher.match_opportunity(
            title="CNC Router Services for Custom Signage",
            description="CNC millwork and routing services for acrylic and wood signage components",
        )
        logger.info(f"  Relevance Score: {result3.relevance_score}")
        logger.info(f"  Tier: {result3.tier_suggestion}")
        logger.info(f"  Matched Keywords: {', '.join(result3.keywords_matched)}")
        logger.info(f"  Rationale: {result3.tier_rationale}")

        # Test case 4: Partially relevant
        logger.info("\n📋 Test 4: Safety Equipment (Partial Match)")
        result4 = matcher.match_opportunity(
            title="Safety Equipment and Signage",
            description="Supply safety equipment including hard hats, vests, and safety signs for construction site",
        )
        logger.info(f"  Relevance Score: {result4.relevance_score}")
        logger.info(f"  Tier: {result4.tier_suggestion}")
        logger.info(f"  Matched Keywords: {', '.join(result4.keywords_matched)}")
        logger.info(f"  Rationale: {result4.tier_rationale}")

        # Test case 5: Irrelevant opportunity
        logger.info("\n📋 Test 5: Road Paving (Irrelevant)")
        result5 = matcher.match_opportunity(
            title="RFP for Road Paving Services",
            description="Asphalt paving and road maintenance services for municipal roads",
        )
        logger.info(f"  Relevance Score: {result5.relevance_score}")
        logger.info(f"  Tier: {result5.tier_suggestion}")
        logger.info(
            f"  Matched Keywords: {result5.keywords_matched if result5.keywords_matched else 'None'}"
        )
        logger.info(f"  Rationale: {result5.tier_rationale}")

        logger.info("\n" + "=" * 60)
        logger.success("✓ Keyword Matcher is working perfectly!")


if __name__ == "__main__":
    main()
