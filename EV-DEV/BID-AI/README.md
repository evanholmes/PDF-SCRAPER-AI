# BID-AI: Intelligent Municipal Bidding System

AI-powered system to monitor, analyze, and win municipal signage and printing contracts across Greater Vancouver and Fraser Valley.

**Built for:** ALL-PRO SIGNS & WESTCOAST CNC

---

## 🚀 Project Status

### ✅ Phase 1: Foundation (Dec 23, 2025)
- [x] Virtual environment setup
- [x] Dependencies installed
- [x] Database schema designed
- [x] Configuration system
- [x] Keyword filtering engine
- [x] Manual monitoring framework
- [ ] Notification system
- [ ] Scraper strategy determination (Day 3)

### 🔄 Current Phase: Architecture & Testing
**Next Steps:**
1. Complete 3-day manual monitoring of BC Bid & MERX
2. Analyze coverage to determine scraper approach
3. Build scrapers (aggregators vs individual portals)
4. Implement THE BID MASTER agent

---

## 📋 Quick Start

### Prerequisites
- Python 3.14+
- PostgreSQL 12+
- Git

### Installation

1. **Clone and navigate to project**
```bash
cd BID-AI
```

2. **Activate virtual environment**
```bash
source venv/bin/activate
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your actual values
nano .env
```

4. **Set up PostgreSQL database**
```bash
# On macOS with Homebrew
brew install postgresql
brew services start postgresql

# Create database
createdb bidai
```

5. **Initialize database**
```bash
python scripts/init_database.py
```

6. **Verify installation**
```bash
python -c "from src.config.settings import get_settings; print('✓ Configuration loaded')"
```

---

## 🏗️ Project Structure

```
BID-AI/
├── README.md                       # This file
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment template
├── .env                           # Your config (git-ignored)
│
├── data/                          # Data files
│   ├── monitoring_log.md          # Manual monitoring tracker
│   └── municipalities/
│       └── bid_portals.csv        # Municipality portal database
│
├── docs/                          # Documentation
│   ├── ARCHITECTURE.md
│   ├── BID_MASTER_PROFILE.md
│   ├── DATABASE_SCHEMA.md         # Database design docs
│   └── ...
│
├── src/                           # Source code
│   ├── config/
│   │   └── settings.py            # Configuration management
│   │
│   ├── database/
│   │   ├── models.py              # SQLAlchemy models
│   │   ├── connection.py          # DB connection manager
│   │   └── schema.sql             # SQL schema definition
│   │
│   ├── filtering/
│   │   └── keyword_matcher.py     # Keyword matching engine
│   │
│   ├── scrapers/                  # Web scrapers (TBD)
│   ├── agents/                    # AI agents (TBD)
│   ├── calendar/                  # Google Calendar integration (TBD)
│   └── dashboard/                 # Visualization dashboard (TBD)
│
├── scripts/                       # Utility scripts
│   └── init_database.py           # Database initialization
│
└── logs/                          # Application logs
```

---

## 🗄️ Database Schema

### Core Tables
- **opportunities**: All bid opportunities from all sources
- **municipalities**: Portal configurations for 31+ entities
- **keywords**: Signage/printing keywords for filtering (40+ terms)
- **bids**: Our bidding activity and outcomes
- **partners**: Network of partner companies
- **activity_log**: Audit trail
- **scraper_runs**: Scraper health monitoring
- **calendar_events**: Google Calendar integration
- **documents**: Bid document storage

### Intelligent Features
- **Full-text search** on opportunity titles and descriptions
- **Automatic relevance scoring** based on keyword matching
- **Tier classification** (A/B/C/D/E) for opportunity routing
- **Trigger-based** timestamp updates
- **Materialized views** for common queries

See `docs/DATABASE_SCHEMA.md` for complete documentation.

---

## 🎯 Keyword Matching & Tier System

### How It Works
The `KeywordMatcher` analyzes opportunity titles and descriptions against 40+ keywords to determine relevance and suggest tier classification.

### Tier Classifications

| Tier | Name | Criteria | Action |
|------|------|----------|--------|
| **A** | Direct Fulfillment | Matches core capabilities (signage/printing/CNC), score ≥30 | Bid directly |
| **B** | Assignment | Relevant but outside direct capabilities, score ≥20 | Find partner, take referral fee |
| **C** | Partnership | Partial capability match, score ≥10 | Joint bid with partner |
| **D** | Brokering | Low relevance but industry-adjacent, score ≥5 | Offer bid-writing services |
| **E** | Archive | Minimal or no relevance | Log for intelligence, move on |

### Example Usage
```python
from src.filtering.keyword_matcher import KeywordMatcher
from src.database.connection import get_session

with get_session() as session:
    matcher = KeywordMatcher(session)
    
    result = matcher.match_opportunity(
        title="RFP for Wayfinding Signage System",
        description="Design and install interior and exterior wayfinding signage..."
    )
    
    print(f"Relevance Score: {result.relevance_score}")
    print(f"Tier: {result.tier_suggestion}")
    print(f"Matched Keywords: {result.keywords_matched}")
```

---

## 📊 Manual Monitoring Protocol

**Objective**: Determine if BC Bid and MERX aggregate most municipal bids, or if individual portal scrapers are needed.

**Process**: Located in `data/monitoring_log.md`
- Check BC Bid and MERX daily for 3 days
- Cross-reference with 3-4 individual municipal portals
- Log findings in monitoring log
- Analyze coverage on Day 3

**Decision Point (Day 3)**:
- If aggregators cover **80%+** → Build BC Bid + MERX scrapers
- If aggregators cover **<80%** → Build individual portal scrapers

---

## 🔧 Configuration

All configuration is managed through environment variables in `.env`:

### Required
- `DATABASE_URL`: PostgreSQL connection string

### Optional but Recommended
- `ANTHROPIC_API_KEY`: For THE BID MASTER AI agent
- `GOOGLE_CALENDAR_CREDENTIALS_PATH`: Calendar integration
- `SMTP_USERNAME` / `SMTP_PASSWORD`: Email notifications
- `BCBID_USERNAME` / `BCBID_PASSWORD`: BC Bid portal access
- `MERX_USERNAME` / `MERX_PASSWORD`: MERX portal access

See `.env.example` for full configuration options.

---

## 🤖 THE BID MASTER

The AI conductor of the BID-AI system. (Under development)

**Responsibilities**:
- Monitor all municipal bid portals
- Filter opportunities by relevance
- Classify into tiers (A/B/C/D/E)
- Deploy specialized agent teams per municipality
- Generate compliant proposals
- Manage partner network
- Report to CEO

---

## 📈 Deal Flow Model

BID-AI implements a multi-tier business model inspired by real estate assignment deals:

### Tier A: Direct Revenue
- Bid and win contracts we can fulfill
- Full margin on work

### Tier B-D: Deal Flow Revenue
- Identify opportunities we can't fulfill
- Match with partners in our network
- Earn referral fees, partnership percentages, or consulting fees
- Build strategic relationships

**Goal**: Generate revenue from ALL municipal signage/printing contracts in the region, not just the ones we can execute.

See `BID-AI.md` for the full strategic vision.

---

## 🗓️ Google Calendar Integration

Each municipality gets its own color-coded calendar for deadline tracking.

**Colors** (from `data/municipalities/bid_portals.csv`):
- Metro Vancouver: #4285F4 (Blue)
- City of Vancouver: #F4B400 (Yellow)
- City of Surrey: #AB47BC (Purple)
- TransLink: #C62828 (Red - Priority)
- etc.

*(Integration code coming in Phase 2)*

---

## 🔍 Scraper Architecture (Pending Day 3 Decision)

### Option A: Aggregator-First Approach
If BC Bid + MERX cover 80%+:
- Primary scrapers: BC Bid, MERX
- Supplementary scrapers: High-value individual portals

### Option B: Platform-Based Approach
If coverage is fragmented:
- Universal BidsAndTenders scraper (17 municipalities)
- Individual scrapers for Direct Website portals
- Custom scrapers for priority targets (TransLink, YVR, BC Hydro)

---

## 🧪 Testing

```bash
# Test database connection
python -m src.database.connection

# Test configuration
python -m src.config.settings

# Test keyword matcher
python -m src.filtering.keyword_matcher
```

---

## 📝 Development Roadmap

### Phase 1: Foundation ✅ (Complete - Dec 23)
- Virtual environment
- Database schema
- Configuration system
- Keyword filtering
- Manual monitoring framework

### Phase 2: Data Collection (Dec 24-26)
- [ ] Complete 3-day manual monitoring
- [ ] Analyze aggregator coverage
- [ ] Decide scraper strategy
- [ ] Build initial scrapers

### Phase 3: Intelligence (Week 2)
- [ ] Implement THE BID MASTER agent
- [ ] Google Calendar integration
- [ ] Email notifications
- [ ] Partner network management

### Phase 4: Automation (Week 3-4)
- [ ] Scheduled scraping (daily runs)
- [ ] Automatic tier classification
- [ ] Proposal generation templates
- [ ] Dashboard for CEO monitoring

### Phase 5: Scale (Month 2+)
- [ ] Partner referral system
- [ ] Bid outcome tracking
- [ ] Win/loss analytics
- [ ] Expand to adjacent trades

---

## 🤝 Contributing

This is a proprietary system for ALL-PRO SIGNS & WESTCOAST CNC.

Development team:
- **CEO**: Strategic oversight, bid decisions
- **Claude (AI Assistant)**: Architecture, development, guidance
- **Evan Holmes**: Development, implementation, operations

---

## 📜 License

Proprietary and Confidential  
ALL-PRO SIGNS & WESTCOAST CNC  
© 2025

---

## 🆘 Troubleshooting

### Database connection fails
```bash
# Check PostgreSQL is running
brew services list

# Verify database exists
psql -l | grep bidai

# Test connection
psql postgresql://localhost/bidai
```

### Import errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Verify dependencies
pip list | grep -E "(sqlalchemy|anthropic|langchain)"
```

### Configuration errors
```bash
# Check .env file exists
ls -la .env

# Validate configuration
python -c "from src.config.settings import get_settings; get_settings().validate_required()"
```

---

## 📞 Support

For questions or issues:
- Check documentation in `docs/`
- Review `data/monitoring_log.md` for research status
- Consult `BID-AI.md` for strategic vision

---

**Built with:**
- Python 3.14
- PostgreSQL
- SQLAlchemy
- Anthropic Claude
- LangChain
- Selenium/Playwright
- Google Calendar API

**Status**: Phase 1 Complete ✅ | Active Development 🚀
