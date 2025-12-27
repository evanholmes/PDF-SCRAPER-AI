# BID-AI System Architecture

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CEO DASHBOARD                                   │
│                    (Full Visibility & Control Interface)                     │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          THE BID MASTER                                 │
│                   AI Conductor & Chief Strategist                       │
│  ┌─────────────────────────────────────────────────────────────────────┐    
│  │ • Orchestrates all municipal agent teams                            │    
│  │ • Prioritizes bid opportunities                                     │    
│  │ • Reviews and approves proposals before submission                  │    
│  │ • Reports to CEO                                                    │    
│  │ • Learns from wins/losses to improve strategy                       │    
│  └─────────────────────────────────────────────────────────────────────┘    │
└────────────────────────────────────────────────────────────────────────────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    ▼                ▼                 ▼
    ┌───────────────────┐ ┌───────────────────┐ ┌───────────────────┐
    │  MUNICIPAL TEAM   │ │  MUNICIPAL TEAM   │ │  MUNICIPAL TEAM   │
    │    Vancouver      │ │     Surrey        │ │   Abbotsford      │
    │                   │ │                   │ │                   │
    │ ┌───────────────┐ │ │ ┌───────────────┐ │ │ ┌───────────────┐ │
    │ │Scout Agent    │ │ │ │Scout Agent    │ │ │ │Scout Agent    │ │
    │ │(Monitor Bids) │ │ │ │(Monitor Bids) │ │ │ │(Monitor Bids) │ │
    │ └───────────────┘ │ │ └───────────────┘ │ │ └───────────────┘ │
    │ ┌───────────────┐ │ │ ┌───────────────┐ │ │ ┌───────────────┐ │
    │ │Analyst Agent  │ │ │ │Analyst Agent  │ │ │ │Analyst Agent  │ │
    │ │(Eval Require.)│ │ │ │(Eval Require.)│ │ │ │(Eval Require.)│ │
    │ └───────────────┘ │ │ └───────────────┘ │ │ └───────────────┘ │
    │ ┌───────────────┐ │ │ ┌───────────────┐ │ │ ┌───────────────┐ │
    │ │Writer Agent   │ │ │ │Writer Agent   │ │ │ │Writer Agent   │ │
    │ │(Draft Propos.)│ │ │ │(Draft Propos.)│ │ │ │(Draft Propos.)│ │
    │ └───────────────┘ │ │ └───────────────┘ │ │ └───────────────┘ │
    │ ┌───────────────┐ │ │ ┌───────────────┐ │ │ ┌───────────────┐ │
    │ │Compliance Agt │ │ │ │Compliance Agt │ │ │ │Compliance Agt │ │
    │ │(Verify Compl.)│ │ │ │(Verify Compl.)│ │ │ │(Verify Compl.)│ │
    │ └───────────────┘ │ │ └───────────────┘ │ │ └───────────────┘ │
    └───────────────────┘ └───────────────────┘ └───────────────────┘
              │                     │                     │
              ▼                     ▼                     ▼
    ┌───────────────────┐ ┌───────────────────┐ ┌───────────────────┐
    │ Vancouver Portal  │ │  Surrey Portal    │ │ Abbotsford Portal │
    │   VendorLink      │ │   Direct Site     │ │  BidsAndTenders   │
    └───────────────────┘ └───────────────────┘ └───────────────────┘
```

---

## 🤖 Agent Hierarchy

### Level 1: THE BID MASTER (Central Command)

**Role:** Chief AI Orchestrator

**Responsibilities:**
- Receives and prioritizes all incoming bid opportunities
- Allocates resources across municipal teams
- Makes go/no-go decisions on bids
- Reviews final proposals before submission
- Maintains institutional knowledge of THE PARENT COMPANY's capabilities
- Reports bid status and pipeline to CEO
- Continuously learns from bid outcomes

**Knowledge Base:**
- THE PARENT COMPANY's complete portfolio
- Pricing structures and cost models
- Historical bid data (wins/losses)
- Competitor intelligence
- Success patterns by municipality

---

### Level 2: Municipal Agent Teams

Each municipality has a dedicated team of specialized agents:

#### 2.1 Scout Agent (The Lookout)
**Mission:** Monitor and detect relevant bid opportunities

**Capabilities:**
- Scrapes assigned bid portal(s)
- Filters by signage/printing keywords
- Detects new postings within hours
- Tracks addenda and amendments
- Monitors Q&A periods
- Alerts team to deadlines

**Output:** Bid Opportunity Reports

---

#### 2.2 Analyst Agent (The Evaluator)
**Mission:** Deep analysis of bid requirements

**Capabilities:**
- Parses RFP/RFQ documents
- Extracts evaluation criteria and weights
- Identifies mandatory requirements
- Assesses technical complexity
- Estimates resource requirements
- Flags risks and concerns
- Compares to THE PARENT COMPANY's capabilities

**Output:** Bid Feasibility Analysis

---

#### 2.3 Writer Agent (The Wordsmith)
**Mission:** Draft compelling, compliant proposals

**Capabilities:**
- Generates executive summaries
- Writes technical approach sections
- Creates project timelines
- Develops pricing narratives
- Incorporates company differentiators
- Tailors language to municipality preferences
- References relevant past projects

**Output:** Draft Proposal Documents

---

#### 2.4 Compliance Agent (The Auditor)
**Mission:** Ensure 100% compliance with requirements

**Capabilities:**
- Verifies all mandatory requirements are addressed
- Checks document formatting requirements
- Validates submission format (PDF, paper, portal)
- Ensures all forms are complete
- Reviews insurance/bonding requirements
- Confirms deadline compliance
- Creates submission checklists

**Output:** Compliance Verification Report

---

## 📊 Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        DATA SOURCES                             │
├─────────────────────────────────────────────────────────────────┤
│  Municipal Portals │ Company Data │ Historical Bids │ Calendar  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      INGESTION LAYER                            │
├─────────────────────────────────────────────────────────────────┤
│  Web Scrapers │ API Connectors │ Document Parser │ OCR Engine   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      PROCESSING LAYER                           │
├─────────────────────────────────────────────────────────────────┤
│  Keyword Filter │ Relevance Scorer │ Deadline Extractor │ NLP   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       STORAGE LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│  Bid Database │ Document Store │ Calendar Events │ Analytics DB │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     APPLICATION LAYER                           │
├─────────────────────────────────────────────────────────────────┤
│  BID MASTER │ Agent Teams │ Dashboard │ Proposal Generator      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                           │
├─────────────────────────────────────────────────────────────────┤
│  CEO Dashboard │ Team Views │ Calendar Interface │ Reports      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🗓️ Calendar Integration Architecture

### Google Calendar Structure

```
BID-AI Calendar System
│
├── 📅 Master Calendar (Overview - CEO View)
│   └── Aggregates all municipal calendars
│
├── 📅 Metro Vancouver - Blue (#4285F4)
│   ├── Bid Opening Events
│   ├── Submission Deadlines
│   └── Q&A Periods
│
├── 📅 City of Vancouver - Yellow (#F4B400)
│   ├── Bid Opening Events
│   ├── Submission Deadlines
│   └── Q&A Periods
│
├── 📅 City of Surrey - Purple (#AB47BC)
│   └── ...
│
├── 📅 City of Burnaby - Cyan (#00ACC1)
│   └── ...
│
└── [One calendar per municipality...]
```

### Event Types

| Event Type | Color Intensity | Description |
|------------|-----------------|-------------|
| New Bid Posted | Light | Opportunity discovered |
| Q&A Period | Medium | Questions can be submitted |
| Q&A Deadline | Medium-Dark | Last day for questions |
| Submission Deadline | Dark/Bold | CRITICAL - submission due |
| Award Announcement | Accent | Expected decision date |

---

## 🔄 Bid Lifecycle Workflow

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   DISCOVER   │ ──▶ │   ANALYZE    │ ──▶│   DECIDE     │
│              │     │              │     │              │
│ Scout finds  │     │ Analyst      │     │ BID MASTER   │
│ new bid      │     │ evaluates    │     │ go/no-go     │
└──────────────┘     └──────────────┘     └──────────────┘
                                                │
                          ┌─────────────────────┤
                          ▼                    ▼
                    ┌──────────┐          ┌──────────┐
                    │   NO-GO  │          │   GO     │
                    │          │          │          │
                    │ Archive  │          │ Proceed  │
                    │ & Learn  │          │          │
                    └──────────┘          └──────────┘
                                                │
                                                ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   SUBMIT     │ ◀── │   REVIEW     │ ◀─-│   DRAFT      │
│              │     │              │     │              │
│ Compliance   │     │ BID MASTER   │     │ Writer       │
│ verified     │     │ approves     │     │ creates      │
└──────────────┘     └──────────────┘     └──────────────┘
       │
       ▼
┌──────────────┐     ┌──────────────┐
│   TRACK      │ ──▶ │   LEARN      │
│              │     │              │
│ Monitor for  │     │ Win/loss     │
│ decision     │     │ analysis     │
└──────────────┘     └──────────────┘
```

---

## 🛠️ Technology Stack (Proposed)

### Backend
- **Language:** Python 3.11+
- **Framework:** FastAPI
- **AI/LLM:** Claude API (Anthropic)
- **Database:** PostgreSQL + Vector DB (pgvector)
- **Task Queue:** Celery + Redis

### Frontend
- **Framework:** Next.js 14 (React)
- **UI Components:** Tailwind CSS + shadcn/ui
- **State Management:** Zustand
- **Charts:** Recharts / D3.js

### Infrastructure
- **Calendar:** Google Calendar API
- **Document Storage:** S3-compatible (MinIO or AWS S3)
- **Scraping:** Playwright / Puppeteer
- **OCR:** Tesseract / AWS Textract

### DevOps
- **Containerization:** Docker
- **Orchestration:** Docker Compose (dev) / Kubernetes (prod)
- **CI/CD:** GitHub Actions
- **Monitoring:** Prometheus + Grafana

---

## 🔐 Security Considerations

1. **Credential Management**
   - All portal credentials stored in encrypted vault
   - Environment variables for API keys
   - Regular credential rotation

2. **Access Control**
   - Role-based access (CEO, BID MASTER, Team)
   - Audit logging of all actions
   - Two-factor authentication for sensitive operations

3. **Data Protection**
   - Encryption at rest and in transit
   - Regular backups
   - PIPEDA compliance for Canadian data

---

## 📈 Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Bid Detection Rate | 100% | Relevant bids found vs. available |
| Response Time | < 24 hrs | Time from posting to team alert |
| Submission Rate | 80%+ | Bids submitted vs. opportunities |
| Win Rate | 30%+ | Contracts won vs. submitted |
| Compliance Rate | 100% | Submissions meeting all requirements |

---

*Architecture Version: 1.0*
*Last Updated: December 2025*
