# CLAUDE.md - BID-AI Project Router

**Navigation guide for Claude Code - Uses router pattern for token efficiency**

## Quick Context

**Project**: BID-AI - AI-powered municipal bidding system for ALL-PRO SIGNS & WESTCOAST CNC  
**Purpose**: Monitor, analyze, and win signage/printing contracts across Greater Vancouver  
**Key Innovation**: Multi-tier deal flow model (monetize ALL opportunities, not just direct bids)

## Development Workflow

**This project uses the PRP (Product Requirement Prompt) methodology.**  
→ For development workflow, read: `METHODOLOGY.md`

Available PRP commands:
- `/prp-planning-create` - Idea → PRD
- `/prp-create` - Requirements → Implementation PRP
- `/prp-base-execute` - Execute BASE PRP
- `/prp-task-execute` - Execute TASK PRP
- `/api-contract-define` - Define API contracts

## Router: IF/THEN Navigation

**IF task involves** → **THEN read**

### Backend Development
- Database models/schema → `src/database/models.py` + `src/database/schema.sql`
- API endpoints → `src/api/` (mirror pattern from existing files)
- Scrapers → `src/scrapers/bcbid_scraper.py` (base pattern)
- Keyword matching → `src/filtering/keyword_matcher.py`
- Tier classification → `src/filtering/bid_classifier.py`
- Configuration → `src/config/settings.py` + `.env`

### Frontend Development
- Dashboard UI → `ui/src/app/page.tsx`
- BC Bid checklist → `ui/src/app/bc-bid-checklist/page.tsx`
- Components → `ui/src/components/` (dark theme pattern)
- Types → `ui/src/types/index.ts`
- Styling → `ui/tailwind.config.ts` (dark theme colors)

### Agent System
- Architecture overview → `docs/ARCHITECTURE.md`
- BID MASTER profile → `docs/BID_MASTER_PROFILE.md`
- Municipality profiles → `municipalities/[city]/profile.md`

### Deal Flow & Strategy
- Tier definitions → `strategy/DEAL_FLOW_MODEL.md`
- Partner network → `strategy/PARTNER_NETWORK.md`

### Database & Testing
- Schema design → `docs/DATABASE_SCHEMA.md`
- Validation commands → `METHODOLOGY.md#validation-standards`

## Quick Commands

### Python Backend
```bash
source venv/bin/activate                    # Activate environment
python scripts/init_database.py             # Initialize database
python -m src.filtering.keyword_matcher     # Test keyword matching
python scripts/test_keyword_matcher.py      # Full keyword test suite
```

### Next.js Frontend
```bash
cd ui && npm run dev        # Dev server (localhost:3000)
cd ui && npm run lint       # Lint frontend
cd ui && npm run build      # Production build
```

### Validation (4 Levels)
```bash
# Level 1: Syntax
ruff check src/ && mypy src/ && cd ui && npm run lint

# Level 2: Unit Tests
pytest tests/ -v && cd ui && npm run test

# Level 3: Integration
curl http://localhost:8000/health && open http://localhost:3000

# Level 4: Creative
python scripts/evaluate_relevance_scoring.py
```

## Tech Stack Quick Reference

| Layer | Technology |
|-------|------------|
| Backend | Python 3.14+, FastAPI, SQLAlchemy 2.0+, PostgreSQL |
| Frontend | Next.js 14, React 18, TypeScript 5.6, Tailwind CSS |
| AI | Anthropic Claude (Sonnet 3.5) |
| Scraping | Selenium, Playwright, BeautifulSoup4 |

## Critical Patterns

### Database Sessions
```python
from src.database.connection import get_db_session

# ✅ ALWAYS use context manager
with get_db_session() as db:
    opportunities = db.query(Opportunity).all()
    db.commit()
```

### Keyword Matching Weights
```python
# Pattern from: src/filtering/keyword_matcher.py
title_score = matches_in_title * 2.0      # 2x weight
category_score = matches_in_category * 3.0 # 3x weight
description_score = matches_in_desc * 1.0  # 1x weight
```

### Frontend Dark Theme
```typescript
// From: ui/src/app/page.tsx
const colors = {
  background: 'bg-[#0a0a0a]',   // Main background
  card: 'bg-[#141414]',          // Card backgrounds
  border: 'border-[#262626]',    // Borders
}
```

## Deal Flow Tiers (A-E)

- **Tier A**: Direct bid (in-house capability)
- **Tier B**: Assignment (refer to partner for finder's fee)
- **Tier C**: Partnership (joint venture)
- **Tier D**: Brokering (consulting/market intelligence)
- **Tier E**: Archive (future reference)

## Agent Hierarchy

```
THE BID MASTER (Central orchestrator)
    └── Municipal Teams (4 agents each)
        ├── Scout (opportunity discovery)
        ├── Analyst (feasibility assessment)
        ├── Writer (proposal generation)
        └── Compliance (requirements verification)
```

## Environment Setup

Required `.env` variables:
- `DATABASE_URL` - PostgreSQL connection
- `ANTHROPIC_API_KEY` - Claude AI API
- `BCBID_USERNAME/PASSWORD` - BC Bid portal credentials

See `.env.example` for complete list.

## Directory Structure

```
BID-AI/
├── src/                    # Python backend
│   ├── api/               # FastAPI endpoints
│   ├── database/          # SQLAlchemy models + schema
│   ├── filtering/         # Keyword matching, tier classification
│   ├── scrapers/          # Municipal portal scrapers
│   └── config/            # Pydantic settings
├── ui/src/                # Next.js frontend
│   ├── app/               # Pages (App Router)
│   ├── components/        # React components
│   └── types/             # TypeScript interfaces
├── workspace/             # PRP workspace
│   ├── PRPs/              # Product Requirement Prompts
│   └── ai_docs/           # Curated documentation
├── docs/                  # Architecture & schema docs
├── municipalities/        # Per-municipality profiles
├── strategy/              # Deal flow & partner network
├── .claude/commands/      # 8 PRP slash commands
└── METHODOLOGY.md         # PRP development workflow
```

## Common Gotchas

1. **Database sessions** - Always use `get_db_session()` context manager
2. **BC Bid portal** - Session expires after 20 min (refresh before scraping)
3. **Claude API** - Rate limit 50 req/min (implement rate limiting)
4. **Frontend routing** - Next.js 14 uses App Router (not Pages Router)
5. **Keyword matching** - Title/category weights differ (2x/3x)

## Getting Started

**New to the project?**
1. Read `METHODOLOGY.md` - Learn PRP workflow
2. Check `docs/ARCHITECTURE.md` - Understand system design
3. Review `src/scrapers/bcbid_scraper.py` - See scraper pattern
4. Look at `ui/src/app/page.tsx` - See dashboard UI pattern

**Adding a feature?**
1. Create INITIAL.md with requirements
2. Run `/prp-create INITIAL.md`
3. Review generated PRP
4. Run `/prp-base-execute [prp-file]`

**Questions about the codebase?**
- Ask Claude to read the specific file from the router above
- Reference METHODOLOGY.md for development patterns
- Check completed PRPs in `workspace/PRPs/completed/`

---

**Token Efficiency Note**: This router keeps CLAUDE.md under 500 lines by pointing to specific files instead of duplicating content. Claude loads detailed context only when needed.
