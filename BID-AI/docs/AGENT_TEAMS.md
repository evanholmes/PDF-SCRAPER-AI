# Agent Team Structure & Configuration

## 🏗️ Team Architecture Overview

Each municipality in the BID-AI system is assigned a dedicated team of AI agents. Teams are configured based on the municipality's bid volume, complexity, and strategic importance.

---

## 🤖 Standard Team Composition

Every municipal team consists of four specialized agents:

```
┌─────────────────────────────────────────────────────────────────┐
│                    MUNICIPAL TEAM STRUCTURE                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│    ┌─────────────────┐         ┌─────────────────┐              │
│    │   SCOUT AGENT   │────────▶│ ANALYST AGENT   │              │
│    │   (Discovery)   │         │  (Evaluation)   │              │
│    └─────────────────┘         └─────────────────┘              │
│            │                           │                        │
│            │                           ▼                       │
│            │                   ┌─────────────────┐              │
│            │                   │  WRITER AGENT   │              │
│            │                   │   (Proposal)    │              │
│            │                   └─────────────────┘              │
│            │                           │                        │
│            │                           ▼                       │
│            │                   ┌─────────────────┐              │
│            └──────────────────▶│COMPLIANCE AGENT │              │
│                                │   (Quality)     │              │
│                                └─────────────────┘              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📋 Agent Role Specifications

### 1. Scout Agent

**Mission:** Continuous monitoring of assigned bid portal(s) for relevant opportunities

**Capabilities:**

| Capability          | Description                                |
|---------------------|--------------------------------------------|
| Portal Monitoring   | Automated scraping at configured intervals |
| Keyword Filtering   | Apply signage/printing keyword rules       |
| New Bid Detection   | Identify and flag new postings             |
| Addenda Tracking    | Monitor for bid amendments                 |
| Q&A Monitoring      | Track question/answer periods              |
| Deadline Extraction | Parse and calendar critical dates          |

**Outputs:**
- Bid Opportunity Alerts
- Portal Status Reports
- Keyword Match Scores
- Calendar Events

**Configuration:**
```yaml
scout_agent:
  scan_interval: 30  # minutes
  keywords: config/keywords.yaml
  alert_threshold: 40  # relevance score
  notification_channels:
    - bid_master
    - team_analyst
```

---

### 2. Analyst Agent

**Mission:** Deep evaluation of bid requirements and feasibility assessment

**Capabilities:**

| Capability          | Description                               |
|---------------------|-------------------------------------------|
| Document Parsing    | Extract requirements from RFP/RFQ PDFs    |
| Criteria Analysis   | Identify evaluation weights and factors   |
| Capability Matching | Compare requirements to company strengths |
| Risk Assessment     | Identify potential challenges             |
| Competitor Analysis | Assess competitive landscape              |
| Win Probability     | Calculate estimated success chance        |

**Outputs:**
- Bid Feasibility Report
- Requirements Checklist
- Risk Assessment Matrix
- Go/No-Go Recommendation

**Configuration:**
```yaml
analyst_agent:
  company_profile: data/company/capabilities.yaml
  competitor_data: data/competitors/
  risk_thresholds:
    high: 7
    medium: 4
    low: 2
  min_capability_match: 0.7
```

---

### 3. Writer Agent

**Mission:** Draft compelling, compliant proposals tailored to each opportunity

**Capabilities:**

| Capability          | Description                      |
|---------------------|----------------------------------|
| Executive Summary   | Write compelling overviews       |
| Technical Approach  | Detail methodology and solutions |
| Experience Section  | Highlight relevant past work     |
| Team Qualifications | Present personnel credentials    |
| Pricing Narrative   | Justify cost proposals           |
| Differentiators     | Emphasize competitive advantages |

**Outputs:**
- Draft Proposal Document
- Supporting Appendices
- Response Matrix
- Revision Suggestions

**Configuration:**
```yaml
writer_agent:
  templates: templates/proposals/
  company_boilerplate: data/company/boilerplate/
  past_projects: data/company/projects/
  tone: professional
  max_iterations: 3
```

---

### 4. Compliance Agent

**Mission:** Ensure 100% compliance with all bid requirements

**Capabilities:**

| Capability               | Description                           |
|--------------------------|---------------------------------------|
| Requirements Checklist   | Track all mandatory items             |
| Format Verification      | Ensure document formatting compliance |
| Completeness Check       | Verify all sections addressed         |
| Form Validation          | Check all required forms completed    |
| Deadline Compliance      | Confirm submission timeline           |
| Submission Prep          | Package final deliverables            |

**Outputs:**
- Compliance Checklist
- Deficiency Report
- Submission Package
- Final Verification Certificate

**Configuration:**
```yaml
compliance_agent:
  checklist_template: templates/compliance/checklist.yaml
  required_documents:
    - proposal
    - pricing
    - certifications
    - insurance
    - references
  verification_steps: 3
```

---

## 🏛️ Team Configurations by Municipality

### Tier 1: High Volume (5+ opportunities/month)

| Municipality      | Team ID  | Priority | Special Config         |
|-------------------|--------- |----------|------------------------|
| City of Vancouver | TEAM-VAN | Critical | VendorLink integration |
| City of Surrey    | TEAM-SUR | Critical | High capacity          |
| Metro Vancouver   | TEAM-MV  | High     | Multi-category         |
| TransLink         | TEAM-TL  | High     | Transit specialty      |

**Tier 1 Configuration:**
```yaml
tier_1_team:
  scout:
    scan_interval: 15  # more frequent
    parallel_scans: true
  analyst:
    priority_processing: true
    deep_analysis: true
  writer:
    senior_templates: true
    custom_voice: true
  compliance:
    multi_reviewer: true
    expedited_review: true
```

---

### Tier 2: Medium Volume (2-4 opportunities/month)

| Municipality | Team ID | Priority | Special Config |
|--------------|---------|----------|----------------|
| City of Burnaby | TEAM-BUR | High | BidsAndTenders |
| City of Richmond | TEAM-RIC | High | Airport proximity |
| City of Coquitlam | TEAM-COQ | Medium | Tri-Cities |
| Township of Langley | TEAM-TOL | Medium | Growth market |
| City of Abbotsford | TEAM-ABB | Medium | Fraser Valley hub |
| Vancouver Airport (YVR) | TEAM-YVR | High | Large contracts |

**Tier 2 Configuration:**
```yaml
tier_2_team:
  scout:
    scan_interval: 30
  analyst:
    standard_processing: true
  writer:
    standard_templates: true
  compliance:
    standard_review: true
```

---

### Tier 3: Low Volume (0-1 opportunities/month)

| Municipality | Team ID | Priority | Special Config |
|--------------|---------|----------|----------------|
| City of New Westminster | TEAM-NW | Medium | Historic focus |
| City of Delta | TEAM-DEL | Low | Agricultural |
| City of North Vancouver | TEAM-CNV | Medium | North Shore |
| District of North Vancouver | TEAM-DNV | Low | Residential |
| City of West Vancouver | TEAM-WV | Medium | Premium |
| City of Port Coquitlam | TEAM-POCO | Low | Tri-Cities |
| City of Port Moody | TEAM-PM | Low | Tri-Cities |
| City of Langley | TEAM-LC | Low | Small city |
| City of Chilliwack | TEAM-CHI | Low | Eastern FV |
| City of Mission | TEAM-MIS | Low | Small |
| District of Maple Ridge | TEAM-MR | Low | Growing |
| City of Pitt Meadows | TEAM-PITM | Low | Small |
| City of White Rock | TEAM-WR | Low | Waterfront |
| District of Hope | TEAM-HOP | Low | Small |
| Harrison Hot Springs | TEAM-HHS | Low | Tourism |
| FVRD | TEAM-FVRD | Medium | Regional |
| Port of Vancouver | TEAM-POV | High | Large contracts |
| BC Hydro | TEAM-BCH | Low | Research |
| BC Ferries | TEAM-BCF | Low | Research |
| UBC | TEAM-UBC | Low | Research |
| SFU | TEAM-SFU | Low | Research |

**Tier 3 Configuration:**
```yaml
tier_3_team:
  scout:
    scan_interval: 60  # hourly
  # Shared resources with other Tier 3 teams
  shared_analyst: true
  shared_writer: true
  compliance:
    batch_review: true
```

---

## 🔄 Team Workflows

### Standard Bid Workflow

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        STANDARD BID WORKFLOW                             │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. DISCOVERY (Scout Agent)                                              │
│     ├─ Detect new bid on portal                                          │
│     ├─ Apply keyword filter                                              │
│     ├─ Calculate relevance score                                         │
│     ├─ If score > threshold:                                             │
│     │   ├─ Create calendar events                                        │
│     │   ├─ Alert BID MASTER                                              │
│     │   └─ Pass to Analyst                                               │
│     └─ If score < threshold:                                             │
│         └─ Log and archive                                               │
│                                                                          │
│  2. ANALYSIS (Analyst Agent)                                             │
│     ├─ Download bid documents                                            │
│     ├─ Parse requirements                                                │
│     ├─ Match to company capabilities                                     │
│     ├─ Assess competition                                                │
│     ├─ Calculate win probability                                         │
│     ├─ Generate feasibility report                                       │
│     └─ Submit GO/NO-GO recommendation to BID MASTER                      │
│                                                                          │
│  3. DECISION (BID MASTER)                                                │
│     ├─ Review analyst recommendation                                     │
│     ├─ Consider portfolio balance                                        │
│     ├─ Assess resource availability                                      │
│     └─ Issue GO or NO-GO decision                                        │
│                                                                          │
│  4. DRAFTING (Writer Agent) [If GO]                                      │
│     ├─ Load bid requirements                                             │
│     ├─ Select appropriate templates                                      │
│     ├─ Draft executive summary                                           │
│     ├─ Write technical approach                                          │
│     ├─ Compile experience/qualifications                                 │
│     ├─ Prepare pricing narrative                                         │
│     └─ Submit draft for review                                           │
│                                                                          │
│  5. REVIEW (BID MASTER)                                                  │
│     ├─ Review draft proposal                                             │
│     ├─ Request revisions if needed                                       │
│     ├─ Approve for compliance check                                      │
│     └─ Flag for CEO review if high-value                                 │
│                                                                          │
│  6. COMPLIANCE (Compliance Agent)                                        │
│     ├─ Verify all requirements addressed                                 │
│     ├─ Check formatting compliance                                       │
│     ├─ Validate all forms complete                                       │
│     ├─ Confirm supporting documents                                      │
│     ├─ Package submission                                                │
│     └─ Issue compliance certificate                                      │
│                                                                          │
│  7. SUBMISSION (Compliance Agent + BID MASTER)                           │
│     ├─ Final BID MASTER approval                                         │
│     ├─ Submit via portal/email/delivery                                  │
│     ├─ Confirm receipt                                                   │
│     └─ Log submission record                                             │
│                                                                          │
│  8. TRACKING (Scout Agent)                                               │
│     ├─ Monitor for award announcement                                    │
│     ├─ Track any requests for clarification                              │
│     └─ Alert team on decision                                            │
│                                                                          │
│  9. LEARNING (All Agents + BID MASTER)                                   │
│     ├─ If WON: Document success factors                                  │
│     ├─ If LOST: Analyze debrief (if available)                           │
│     └─ Update knowledge base                                             │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Team Performance Metrics

### Scout Agent Metrics
| Metric | Target | Measurement |
|--------|--------|-------------|
| Detection Rate | 100% | Relevant bids found / available |
| False Positive Rate | < 20% | Irrelevant flagged / total flagged |
| Alert Latency | < 4 hrs | Time from posting to alert |
| Portal Coverage | 100% | Successful scans / scheduled scans |

### Analyst Agent Metrics
| Metric | Target | Measurement |
|--------|--------|-------------|
| Analysis Completion | < 24 hrs | Time from alert to recommendation |
| Accuracy | > 80% | Correct GO/NO-GO vs. outcome |
| Requirement Coverage | 100% | Requirements identified / actual |
| Report Quality | > 4/5 | BID MASTER rating |

### Writer Agent Metrics
| Metric | Target | Measurement |
|--------|--------|-------------|
| Draft Completion | < 5 days | Time from GO to first draft |
| Revision Cycles | < 2 | Drafts before approval |
| Compliance Pass Rate | > 90% | First-time compliance approval |
| Proposal Quality | > 4/5 | BID MASTER rating |

### Compliance Agent Metrics
| Metric | Target | Measurement |
|--------|--------|-------------|
| Review Time | < 24 hrs | Time from draft to verification |
| Defect Detection | > 95% | Issues caught / total issues |
| On-Time Submission | 100% | Submitted before deadline |
| Compliance Rate | 100% | Submissions meeting all requirements |

---

## 🛠️ Team Configuration Templates

### team_config.yaml Structure

```yaml
# Team Configuration Template
team:
  id: "TEAM-XXX"
  municipality: "City of Example"
  region: "Metro Vancouver"  # or "Fraser Valley"
  tier: 2  # 1, 2, or 3
  portal:
    url: "https://example.bidsandtenders.ca"
    type: "bidsandtenders"  # or "direct", "vendorlink", "custom"
    credentials:
      username: "${TEAM_XXX_USERNAME}"
      password: "${TEAM_XXX_PASSWORD}"
  calendar:
    id: "calendar_id@group.calendar.google.com"
    color: "#AB47BC"
  
  agents:
    scout:
      enabled: true
      scan_interval: 30  # minutes
      keywords_profile: "standard"  # or "extended"
      alert_threshold: 40
      
    analyst:
      enabled: true
      auto_analyze: true
      capability_threshold: 0.7
      risk_tolerance: "medium"
      
    writer:
      enabled: true
      template_set: "standard"
      custom_sections: []
      
    compliance:
      enabled: true
      checklist_version: "2025.1"
      auto_package: true
      
  notifications:
    bid_master: true
    email: "bids@parentcompany.com"
    slack: "#team-xxx-alerts"
```

---

## 🔗 Inter-Team Communication

### Team-to-BID MASTER

```
Municipal Team ──────▶ BID MASTER
     │
     ├─ New Opportunity Alerts
     ├─ Analysis Reports
     ├─ GO/NO-GO Recommendations
     ├─ Draft Proposals (for review)
     ├─ Compliance Certificates
     └─ Submission Confirmations
```

### BID MASTER-to-Team

```
BID MASTER ──────▶ Municipal Team
     │
     ├─ GO/NO-GO Decisions
     ├─ Priority Assignments
     ├─ Revision Requests
     ├─ Resource Allocations
     ├─ Deadline Reminders
     └─ Strategic Guidance
```

### Cross-Team Sharing

```
Team A ◀──────▶ Team B
     │
     ├─ Template Sharing
     ├─ Best Practices
     ├─ Competitor Intelligence
     └─ Lessons Learned
```

---

## 🚀 Team Activation Sequence

### New Team Setup

1. **Portal Setup**
   - Create account on bid portal (if required)
   - Configure scraper authentication
   - Test portal connectivity

2. **Calendar Setup**
   - Create Google Calendar
   - Apply color coding
   - Share with BID MASTER and CEO

3. **Agent Configuration**
   - Deploy Scout Agent
   - Configure keywords
   - Set alert thresholds

4. **Testing**
   - Run initial portal scan
   - Verify keyword filtering
   - Test alert delivery

5. **Activation**
   - Enable continuous monitoring
   - Add to BID MASTER oversight
   - Begin tracking metrics

---

*Agent Teams Documentation Version: 1.0*
*Last Updated: December 2025*
