#!/usr/bin/env python3
"""
Initialize the BID-AI database
- Creates all tables
- Loads seed data from CSV
- Sets up initial configuration
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import csv

from loguru import logger

from src.config.settings import get_settings
from src.database.connection import init_db
from src.database.models import Municipality


def load_municipalities_from_csv(db):
    """Load municipalities from the CSV file"""
    csv_path = project_root / "data" / "municipalities" / "bid_portals.csv"

    if not csv_path.exists():
        logger.warning(f"Municipality CSV not found: {csv_path}")
        return

    logger.info(f"Loading municipalities from {csv_path}")

    with db.get_session() as session:
        count = 0

        with open(csv_path, "r") as f:
            reader = csv.DictReader(f)

            for row in reader:
                # Check if municipality already exists
                existing = (
                    session.query(Municipality)
                    .filter_by(name=row["Municipality/Organization"])
                    .first()
                )

                if existing:
                    logger.debug(
                        f"Municipality already exists: {row['Municipality/Organization']}"
                    )
                    continue

                # Create new municipality
                municipality = Municipality(
                    name=row["Municipality/Organization"],
                    region=row["Region"],
                    portal_name=row["Portal Name"],
                    portal_url=row["Portal URL"],
                    portal_type=row["Portal Type"],
                    account_required=row["Account Required"].lower() == "yes",
                    calendar_color=row.get("Calendar Color", "#4285F4"),
                    monitoring_status=row.get("Status", "active"),
                    agent_team_assigned=row.get("Team Assigned"),
                    notes=row.get("Notes", ""),
                )

                session.add(municipality)
                count += 1

        logger.success(f"Loaded {count} municipalities")


def main():
    """Main initialization function"""
    logger.info("=" * 60)
    logger.info("BID-AI Database Initialization")
    logger.info("=" * 60)

    # Load settings
    try:
        settings = get_settings()
        logger.info(f"✓ Settings loaded")
        logger.info(f"  Database: {settings.database.url}")
    except Exception as e:
        logger.error(f"Failed to load settings: {e}")
        logger.error("Make sure you've created a .env file (copy from .env.example)")
        sys.exit(1)

    # Initialize database
    try:
        db = init_db(settings.database.url)
        logger.info(f"✓ Database manager initialized")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        sys.exit(1)

    # Create tables
    try:
        logger.info("Creating database tables...")
        db.create_all_tables()
        logger.success("✓ All tables created")
    except Exception as e:
        logger.error(f"Failed to create tables: {e}")
        sys.exit(1)

    # Execute schema SQL file (for triggers, functions, views)
    try:
        schema_path = project_root / "src" / "database" / "schema.sql"
        if schema_path.exists():
            logger.info("Executing schema SQL file...")
            db.execute_sql_file(str(schema_path))
            logger.success("✓ Schema SQL executed")
        else:
            logger.warning(f"Schema SQL file not found: {schema_path}")
    except Exception as e:
        logger.warning(f"Could not execute schema SQL (this may be okay): {e}")

    # Load municipalities
    try:
        load_municipalities_from_csv(db)
        logger.success("✓ Municipalities loaded")
    except Exception as e:
        logger.error(f"Failed to load municipalities: {e}")

    # Verify setup
    try:
        with db.get_session() as session:
            from src.database.models import Keyword, Municipality

            muni_count = session.query(Municipality).count()
            keyword_count = session.query(Keyword).count()

            logger.info("")
            logger.info("=" * 60)
            logger.info("Database Setup Complete!")
            logger.info("=" * 60)
            logger.info(f"  Municipalities: {muni_count}")
            logger.info(f"  Keywords: {keyword_count}")
            logger.info("")
            logger.success("✓ BID-AI is ready to start monitoring bids!")

    except Exception as e:
        logger.error(f"Verification failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
