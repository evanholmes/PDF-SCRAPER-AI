# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BID-AI is an AI-powered municipal bidding system for **ALL-PRO SIGNS & WESTCOAST CNC** that monitors, analyzes, and helps win signage/printing contracts across Greater Vancouver and Fraser Valley. Beyond direct bidding, it implements a **multi-tier deal flow model** that creates value from ALL opportunities by matching unsuitable bids with partner companies for referral fees.

## Development Commands

### Python Backend
```bash
# Activate environment
source venv/bin/activate

# Database initialization
python scripts/init_database.py

# Test configuration
python -c "from src.config.settings import get_settings; print('✓ Config loaded')"

# Test keyword matching
python -m src.filtering.keyword_matcher
python scripts/test_keyword_matcher.py
```

### Next.js Frontend (in /ui directory)
```bash
npm run dev      # Development server (localhost:3000)
npm run build    # Production build
npm run start    # Production server
npm run lint     # Linting
```

## Architecture

### Agent Hierarchy
- **THE BID MASTER**: Central AI orchestrator overseeing all municipalities
- **Municipal Teams**: 4-agent teams per municipality (Scout, Analyst, Writer, Compliance)
- Each municipality has its own agent team that reports to THE BID MASTER

### Deal Flow Tiers
- **Tier A (Direct)**: Bid directly on matching opportunities
- **Tier B (Assignment)**: Refer to partners for finder's fee
- **Tier C (Partnership)**: Joint ventures with partners
- **Tier D (Brokering)**: Consulting fees for market intelligence
- **Tier E (Archive)**: Document for future reference

### Tech Stack
- **Backend**: Python 3.14+, SQLAlchemy 2.0+, PostgreSQL, Anthropic Claude
- **Frontend**: Next.js 14, React 18, TypeScript 5.6, Tailwind CSS
- **Scraping**: Selenium, Playwright, Scrapy, BeautifulSoup4

## Code Structure

```
src/                    # Python backend
├── config/settings.py  # Pydantic config (singleton via get_settings())
├── database/
│   ├── models.py       # SQLAlchemy ORM (municipalities, opportunities, partners, bids)
│   ├── connection.py   # Database session management with context managers
│   └── schema.sql      # SQL triggers for relevance scoring, full-text search
├── filtering/
│   ├── keyword_matcher.py    # Weighted keyword matching (40+ terms)
│   ├── capability_matcher.py # Equipment capability verification
│   └── bid_classifier.py     # Tier classification engine

ui/src/                 # Next.js frontend
├── app/
│   ├── page.tsx        # CEO Dashboard
│   └── bc-bid-checklist/  # BC Bid requirements checklist
├── components/
│   ├── shared/Sidebar.tsx  # Navigation
│   └── BCBidChecklist.tsx  # Interactive checklist with localStorage
├── types/index.ts      # TypeScript interfaces (Bid, Municipality, Agent, Partner)
└── lib/utils.ts        # cn() utility for Tailwind class merging
```

## Key Patterns

### Keyword Matching
Weighted scoring: title matches (2x), category matches (3x), description (1x). Keywords include signage, wayfinding, printing, CNC-related terms. Relevance scores 0-100.

### Database Sessions
Always use context managers for database operations:
```python
with get_db_session() as db:
    # operations here
    db.commit()
```

### Frontend Styling
Dark theme with Tailwind: `bg-[#0a0a0a]` base, `bg-[#141414]` cards, `border-[#262626]` borders. Use `cn()` from lib/utils for conditional classes.

## Configuration

Required `.env` variables (see `.env.example`):
- `DATABASE_URL`: PostgreSQL connection string
- `ANTHROPIC_API_KEY`: Claude AI API key
- `BCBID_USERNAME/PASSWORD`: BC Bid portal credentials
- `GOOGLE_CALENDAR_CREDENTIALS_PATH`: For deadline tracking

## Documentation

- `/docs/ARCHITECTURE.md`: Full system architecture and agent hierarchy
- `/docs/DATABASE_SCHEMA.md`: Complete database design (9 core tables)
- `/docs/BID_MASTER_PROFILE.md`: AI orchestrator role definition
- `/municipalities/`: Tiered profiles for 31+ municipalities
- `/strategy/`: Deal flow model and partner network strategy
