#!/usr/bin/env python3
"""
Load keywords into the database
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from loguru import logger

from src.config.settings import get_settings
from src.database.connection import init_db
from src.database.models import Keyword

keywords_data = [
    ("signage", "signage", 10),
    ("wayfinding", "signage", 10),
    ("sign", "signage", 8),
    ("dimensional letters", "signage", 10),
    ("monument sign", "signage", 10),
    ("pylon sign", "signage", 10),
    ("channel letters", "signage", 10),
    ("illuminated sign", "signage", 9),
    ("digital signage", "signage", 9),
    ("directional signs", "signage", 8),
    ("building signage", "signage", 8),
    ("exterior signage", "signage", 8),
    ("interior signage", "signage", 8),
    ("ADA signage", "signage", 7),
    ("braille signage", "signage", 7),
    ("safety signs", "signage", 6),
    ("parking signs", "signage", 6),
    ("traffic signs", "signage", 5),
    ("printing", "printing", 10),
    ("print", "printing", 8),
    ("digital printing", "printing", 9),
    ("large format printing", "printing", 10),
    ("offset printing", "printing", 8),
    ("banners", "printing", 8),
    ("posters", "printing", 7),
    ("vinyl graphics", "printing", 9),
    ("decals", "printing", 7),
    ("vehicle wrap", "printing", 8),
    ("window graphics", "printing", 8),
    ("floor graphics", "printing", 7),
    ("wall murals", "printing", 8),
    ("CNC", "fabrication", 9),
    ("millwork", "fabrication", 9),
    ("router", "fabrication", 7),
    ("acrylic", "materials", 7),
    ("aluminum", "materials", 6),
    ("bronze", "materials", 6),
    ("wood", "materials", 5),
]


def main():
    settings = get_settings()
    db = init_db(settings.database.url)

    logger.info("Loading keywords into database...")

    with db.get_session() as session:
        count = 0
        for keyword, category, weight in keywords_data:
            existing = session.query(Keyword).filter_by(keyword=keyword).first()
            if not existing:
                kw = Keyword(keyword=keyword, category=category, weight=weight)
                session.add(kw)
                count += 1

        logger.success(f"Added {count} keywords")

        total = session.query(Keyword).count()
        logger.info(f"Total keywords in database: {total}")


if __name__ == "__main__":
    main()
