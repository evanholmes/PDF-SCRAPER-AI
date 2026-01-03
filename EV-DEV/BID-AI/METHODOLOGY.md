# BID-AI Development Methodology

**Using Product Requirement Prompts (PRPs) for Municipal Bidding System Development**

## Overview

BID-AI uses the **PRP (Product Requirement Prompt) methodology** for all feature development, agent creation, and system transformations. This ensures consistent, validated, first-pass implementations across our multi-municipality bidding platform.

## Quick Start

### Available Commands

All PRP commands are available in `.claude/commands/`:

| Command | Purpose | Use For |
|---------|---------|---------|
| `/prp-planning-create` | Idea → PRD | New municipality integrations, complex features |
| `/prp-create` | Requirements → PRP | Standard feature development |
| `/prp-base-execute` | Execute BASE PRP | Implementing new endpoints, UI components |
| `/prp-spec-execute` | Execute SPEC PRP | Database migrations, framework upgrades |
| `/prp-task-execute` | Execute TASK PRP | Multi-phase rollouts, agent hierarchy |
| `/task-list-init` | Create task lists | Complex projects with milestones |
| `/api-contract-define` | Define API contracts | Backend/Frontend integration |
| `/read-docs` | Load context | Project documentation |

### Directory Structure

```
BID-AI/
├── workspace/
│   ├── PRPs/
│   │   ├── in-progress/        # Active PRPs being executed
│   │   └── completed/          # Finished PRPs (reference library)
│   └── ai_docs/                # Curated documentation
├── CLAUDE.md                   # Router pattern navigation
├── METHODOLOGY.md              # This file
└── .claude/commands/           # 8 PRP slash commands
```

## BID-AI-Specific Patterns

### 1. Municipality Integration Pattern

When adding new municipalities, use **PLANNING PRP** → **BASE PRP** flow:

```bash
# Step 1: Research and plan
/prp-planning-create "Integrate City of Surrey bidding portal"

# Step 2: Generate implementation PRP
/prp-create workspace/PRPs/in-progress/surrey-integration-PRD.md

# Step 3: Execute
/prp-base-execute workspace/PRPs/in-progress/surrey-integration-PRP.md
```

**Required Context for Municipality PRPs**:
- Portal URL and login credentials (from .env)
- Existing scraper pattern: `src/scrapers/bcbid_scraper.py`
- Database model: `src/database/models.py:Municipality`
- Tier classification logic: `src/filtering/bid_classifier.py`

### 2. Agent Creation Pattern

For creating new municipal agent teams (Scout, Analyst, Writer, Compliance):

```bash
# Step 1: Create task list for agent hierarchy
/task-list-init "Create 4-agent team for City of Vancouver"

# Step 2: Execute with validation at each step
/prp-task-execute workspace/PRPs/in-progress/vancouver-agents-tasks.md
```

**Required Context for Agent PRPs**:
- Agent architecture: `docs/ARCHITECTURE.md`
- BID MASTER profile: `docs/BID_MASTER_PROFILE.md`
- Municipality profile: `municipalities/[city]/profile.md`
- Claude API integration: `src/config/settings.py:ANTHROPIC_API_KEY`

### 3. Deal Flow Tier Implementation

When implementing tier classification (A-E):

```yaml
Goal: Implement Tier B (Assignment) deal flow

Context:
  - file: src/filtering/bid_classifier.py
    why: Existing tier classification logic
  - file: src/database/models.py:Partner
    why: Partner network data model
  - url: CLAUDE.md#deal-flow-tiers
    why: Business rules for tier assignment
  - gotcha: "Tier B requires partner capability matching before assignment"
    solution: "Use src/filtering/capability_matcher.py for validation"

Validation:
  Level 1: pytest tests/test_classifier.py::test_tier_b_assignment
  Level 2: python scripts/test_tier_assignment.py
  Level 3: Check UI at http://localhost:3000/opportunities?tier=B
```

### 4. Scraper Development Pattern

When building new scrapers or updating existing ones:

```yaml
Pattern: MIRROR from src/scrapers/bcbid_scraper.py

Keep:
  - Rate limiting (SCRAPER_RATE_LIMIT_SECONDS)
  - Error handling pattern (try/except with logging)
  - Selenium setup (headless mode, user agent)
  - Database session management (get_db_session context manager)

Modify:
  - Portal URL and selectors
  - Login flow (if different)
  - Parsing logic for opportunity fields

Gotchas:
  - BC Bid uses dynamic loading → wait for ElementClickableInterceptedException
  - MERX has bot detection → rotate user agents
  - Some municipalities require VPN → document in portal profile
```

### 5. Frontend-Backend Integration

When connecting Next.js UI to Python API:

```bash
# Define contract first
/api-contract-define "User dashboard analytics endpoint"

# Then implement with validated contract
/prp-create workspace/PRPs/in-progress/dashboard-api-contract.md
```

**Standard BID-AI API Pattern**:
```python
# Backend: src/api/opportunities.py
from fastapi import APIRouter, Depends
from src.database.connection import get_db_session

router = APIRouter(prefix="/api/v1/opportunities")

@router.get("/", response_model=List[OpportunityResponse])
async def list_opportunities(
    tier: Optional[str] = None,
    db: Session = Depends(get_db_session)
):
    # Implementation following src/api/bids.py pattern
    pass
```

```typescript
// Frontend: ui/src/app/opportunities/page.tsx
// MIRROR pattern from: ui/src/app/bc-bid-checklist/page.tsx
async function fetchOpportunities(tier?: string) {
  const res = await fetch(`/api/v1/opportunities?tier=${tier}`)
  if (!res.ok) throw new Error('Failed to fetch')
  return res.json()
}
```

## BID-AI Validation Standards

### Level 1: Syntax (Fast - Run Always)

```bash
# Python Backend
cd /path/to/BID-AI
source venv/bin/activate
ruff check src/ tests/
mypy src/

# Next.js Frontend
cd ui
npm run lint
npm run typecheck
```

### Level 2: Unit Tests (Minutes)

```bash
# Python
pytest tests/ -v --cov=src

# Next.js
cd ui
npm run test
```

### Level 3: Integration (Manual)

```bash
# Backend health check
curl http://localhost:8000/health

# Test scraper
python -m src.scrapers.bcbid_scraper

# Test keyword matching
python scripts/test_keyword_matcher.py

# Frontend
open http://localhost:3000
```

### Level 4: Creative (Domain-Specific)

```bash
# Bid relevance accuracy
python scripts/evaluate_relevance_scoring.py

# Scraper reliability (run overnight)
python scripts/test_scraper_reliability.py --duration=24h

# Agent decision quality
python scripts/evaluate_agent_recommendations.py

# Deal flow accuracy
python scripts/validate_tier_classifications.py
```

## Common BID-AI Gotchas

### 1. Database Sessions

**CRITICAL**: Always use context managers for DB operations

```python
# ✅ CORRECT
from src.database.connection import get_db_session

with get_db_session() as db:
    opportunities = db.query(Opportunity).all()
    db.commit()

# ❌ WRONG
db = get_db_session()  # Session leak!
opportunities = db.query(Opportunity).all()
```

### 2. Keyword Matching Weights

**GOTCHA**: Title matches are 2x, category matches are 3x

```python
# Pattern from: src/filtering/keyword_matcher.py
title_score = matches_in_title * 2.0
category_score = matches_in_category * 3.0
description_score = matches_in_description * 1.0
total = (title_score + category_score + description_score) / total_keywords * 100
```

### 3. Anthropic API Rate Limits

**GOTCHA**: Claude API has rate limits (50 req/min for Sonnet)

```python
# Solution: Implement rate limiting in agent calls
# See: src/agents/base_agent.py for RateLimiter usage
from src.utils.rate_limiter import RateLimiter

limiter = RateLimiter(max_calls=40, time_window=60)
async def call_claude():
    await limiter.acquire()
    response = await anthropic.messages.create(...)
```

### 4. BC Bid Portal Quirks

**GOTCHA**: BC Bid session expires after 20 minutes of inactivity

```python
# Solution: Refresh session before scraping
# Pattern from: src/scrapers/bcbid_scraper.py

def scrape():
    login()
    last_activity = time.time()

    for page in pages:
        if time.time() - last_activity > 1000:  # 16.6 min
            login()  # Refresh session
        scrape_page(page)
        last_activity = time.time()
```

### 5. Frontend Dark Theme Colors

**PATTERN**: Consistent dark theme across all UI

```typescript
// From: ui/src/app/page.tsx and ui/tailwind.config.ts
const colors = {
  background: 'bg-[#0a0a0a]',     // Main background
  card: 'bg-[#141414]',            // Card backgrounds
  border: 'border-[#262626]',      // Borders
  text: 'text-white',              // Primary text
  textMuted: 'text-gray-400',      // Secondary text
}

// Use cn() utility for conditional classes
import { cn } from '@/lib/utils'
<div className={cn('bg-[#141414]', isActive && 'border-blue-500')} />
```

## Example: Adding New Municipality (Complete Flow)

### Step 1: Create INITIAL.md

```markdown
# Add City of Burnaby Bidding Portal

## Requirements
- Scrape opportunities from Burnaby's municipal portal
- Classify opportunities into tiers A-E
- Create 4-agent team (Scout, Analyst, Writer, Compliance)
- Integrate with existing dashboard

## Context
- Portal URL: https://burnaby.ca/business/bids-tenders
- Similar to: Surrey (uses same platform)
- Profile tier: Tier 2 (medium priority municipality)
```

### Step 2: Generate Planning PRP

```bash
/prp-planning-create workspace/PRPs/in-progress/burnaby-INITIAL.md
```

Claude researches:
- Burnaby portal structure
- Similar municipality implementations
- Required database changes
- Agent configuration needs

Output: `burnaby-integration-PRD.md` with complete specs

### Step 3: Generate Implementation PRP

```bash
/prp-create workspace/PRPs/in-progress/burnaby-integration-PRD.md
```

Output: `burnaby-integration-PRP.md` with:
- Complete context (URLs, file paths, patterns)
- Task list with CREATE/MODIFY keywords
- Pseudocode for scraper logic
- 4-level validation loop
- Integration with existing codebase

### Step 4: Execute

```bash
/prp-base-execute workspace/PRPs/in-progress/burnaby-integration-PRP.md
```

Claude:
1. Creates scraper following bcbid_scraper.py pattern
2. Adds Municipality model entry
3. Creates agent team configuration
4. Adds UI components for Burnaby opportunities
5. Runs validation loop (syntax → unit → integration → creative)
6. Iterates on test failures
7. Marks tasks [DONE]

### Step 5: Archive

```bash
mv workspace/PRPs/in-progress/burnaby-* workspace/PRPs/completed/
```

## Best Practices for BID-AI PRPs

### 1. Always Reference Existing Patterns

```yaml
# ✅ GOOD
CREATE src/scrapers/burnaby_scraper.py:
  - MIRROR pattern from: src/scrapers/bcbid_scraper.py (lines 45-120)
  - KEEP: Rate limiting, error handling, session management
  - MODIFY: Portal URL, selectors for Burnaby's HTML structure
```

### 2. Document Municipality-Specific Quirks

```yaml
# ✅ GOOD
Gotchas for Burnaby Portal:
  - Uses JavaScript rendering → Selenium required (not BeautifulSoup)
  - Login redirects to SSO → capture redirect URL before auth
  - Opportunities listed across multiple tabs → scrape all 4 tabs
  - Date format: DD/MM/YYYY (not MM/DD/YYYY like BC Bid)
```

### 3. Include Business Context

```yaml
# ✅ GOOD
Why: Burnaby is Tier 2 priority municipality (population 250k+, high signage volume)
Success: 90%+ relevant opportunities captured, <5% false positives
Impact: Estimated 15-20 monthly opportunities, $50k-$200k contract values
```

### 4. Validate Against Real Data

```yaml
# ✅ GOOD
Level 3 - Integration:
  RUN: python -m src.scrapers.burnaby_scraper --test-mode
  EXPECT: ≥10 opportunities found, all have required fields populated
  IF_FAIL: Check logs/burnaby_scraper.log for parsing errors

Level 4 - Business Logic:
  RUN: python scripts/evaluate_burnaby_relevance.py
  EXPECT: ≥85% accuracy on manually labeled test set
  IF_FAIL: Review keywords in src/filtering/keyword_matcher.py
```

## Templates Location

All PRP templates are in: `claude-prp-methodology/templates/`

- `BASE_PRP_TEMPLATE.md` - Standard feature development
- `PLANNING_PRP_TEMPLATE.md` - Idea → PRD transformation
- `SPEC_PRP_TEMPLATE.md` - System transformations
- `TASK_LIST_TEMPLATE.md` - Complex project breakdown
- `API_CONTRACT_TEMPLATE.md` - Backend/Frontend contracts

Copy and customize for BID-AI features.

## Learning Resources

- **Full methodology**: `claude-prp-methodology/METHODOLOGY.md`
- **Setup guide**: `claude-prp-methodology/SETUP.md`
- **Best practices**: `claude-prp-methodology/docs/BEST_PRACTICES.md`
- **Examples**: `claude-prp-methodology/examples/`

## Quick Reference

### When to Use Each PRP Type

| Scenario | PRP Type | Command |
|----------|----------|---------|
| "Add new municipality" | PLANNING → BASE | `/prp-planning-create` |
| "Build analytics dashboard" | BASE | `/prp-create` |
| "Migrate SQLite → PostgreSQL" | SPEC | `/prp-spec-execute` |
| "Rollout to 10 municipalities" | TASK | `/task-list-init` |
| "Add API endpoint + UI" | BASE + API Contract | `/api-contract-define` |

### Validation Loop Quick Reference

```bash
# Level 1: Syntax (5 seconds)
ruff check src/ && mypy src/ && cd ui && npm run lint

# Level 2: Unit Tests (1-2 minutes)
pytest tests/ -v && cd ui && npm run test

# Level 3: Integration (2-5 minutes)
python scripts/test_keyword_matcher.py && curl http://localhost:8000/health

# Level 4: Creative (varies)
python scripts/evaluate_[feature].py
```

---

**Remember**: Good PRPs = First-pass success. Invest time in context, save time in iterations.
