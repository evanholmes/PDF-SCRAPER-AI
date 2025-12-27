# City of Surrey - Municipality Profile

## 🏛️ Basic Information

| Field | Value |
|-------|-------|
| **Official Name** | City of Surrey |
| **Region** | Metro Vancouver |
| **Population** | ~600,000 (BC's second largest city) |
| **Team ID** | TEAM-SUR |
| **Tier** | 1 - Critical |
| **Calendar Color** | #AB47BC (Purple) |
| **Status** | Active |

---

## 🌐 Bid Portal Information

### Primary Portal: City of Surrey Website

| Field | Value |
|-------|-------|
| **Portal Name** | Tenders, RFQs & RFPs |
| **Portal URL** | https://www.surrey.ca/business-economy/tenders-rfqs-rfps |
| **Portal Type** | Direct Website |
| **Account Required** | To Be Verified |
| **Username** | [TO BE CONFIGURED] |
| **Password** | [SECURE STORAGE] |

### Portal Features
- Direct document downloads
- Contact information per tender
- Award notifications posted
- Q&A via email

### Relevant Categories to Monitor
- General Construction
- Parks & Recreation
- Transportation & Infrastructure
- Facilities Management
- Professional Services

---

## 📋 Procurement Process

### Bid Types Used
- **RFP** (Request for Proposal)
- **RFQ** (Request for Quotation)
- **ITT** (Invitation to Tender)
- **RFPQ** (Request for Pre-Qualification)

### Typical Evaluation Criteria

| Criteria | Typical Weight |
|----------|----------------|
| Technical Merit | 35-45% |
| Experience | 20-25% |
| Price | 25-35% |
| Project Approach | 10-15% |

### Standard Requirements
- Valid Business License
- WorkSafeBC Registration
- Minimum Insurance Coverage ($2M-$5M)
- Bonding (for larger projects)
- References from similar projects

---

## 📅 Calendar Configuration

### Google Calendar Details
| Field | Value |
|-------|-------|
| Calendar Name | BID-AI: City of Surrey |
| Calendar ID | [TO BE CREATED] |
| Color | #AB47BC (Purple) |
| Time Zone | America/Vancouver |

### Event Prefix
All events use prefix: `SUR-[YEAR]-[NUMBER]`  
Example: `SUR-2025-089`

---

## 🤖 Agent Team Configuration

### Team: TEAM-SUR

```yaml
team_id: TEAM-SUR
municipality: City of Surrey
tier: 1
priority: critical

scout_agent:
  scan_interval: 15  # minutes
  portal_url: https://www.surrey.ca/business-economy/tenders-rfqs-rfps
  keywords_profile: extended
  alert_threshold: 35
  scraper_type: direct_website

analyst_agent:
  priority_processing: true
  deep_analysis: true
  capability_threshold: 0.65
  growth_market: true  # Flag for rapidly growing city

writer_agent:
  template_set: surrey-custom
  tone: professional-growth
  emphasize_capacity: true  # Growing city values capacity

compliance_agent:
  checklist: surrey-standard
  multi_reviewer: true
  insurance_minimum: 2000000
```

---

## 🏢 Key Departments & Contacts

### Procurement Services
- **Department:** Finance - Purchasing
- **General Inquiries:** Via tender documents
- **Website:** https://www.surrey.ca/business-economy/tenders-rfqs-rfps

### Relevant Departments for Signage
- **Parks, Recreation & Culture** - Park and trail signage
- **Engineering** - Traffic and street signage
- **Planning & Development** - Development signage
- **Transportation** - Transit and wayfinding

---

## 📊 Historical Data

### Past Signage/Printing Opportunities (Known)
| Year | Opportunity | Value | Outcome |
|------|-------------|-------|---------|
| 2025 | TBD | TBD | TBD |

*To be populated as data is gathered*

### Win/Loss Record
| Metric | Value |
|--------|-------|
| Total Bids Submitted | 0 |
| Wins | 0 |
| Losses | 0 |
| Win Rate | N/A |

---

## 📁 Folder Contents

```
surrey/
├── PROFILE.md (this file)
├── portal-docs/
│   ├── procurement-guidelines.pdf
│   └── vendor-requirements.pdf
├── bids-active/
│   └── [active bid folders]
├── bids-archive/
│   └── [completed/passed bid folders]
├── proposals/
│   └── [submitted proposals]
├── templates/
│   └── surrey-proposal-template.md
└── research/
    ├── growth-analysis.md
    ├── new-developments.md
    └── competitor-analysis.md
```

---

## 🔗 Important Links

- **Main Procurement Page:** https://www.surrey.ca/business-economy/tenders-rfqs-rfps
- **Doing Business with Surrey:** https://www.surrey.ca/business-economy
- **City News & Updates:** https://www.surrey.ca/news

---

## 📝 Notes & Intelligence

### Strategic Importance
Surrey is BC's second-largest and fastest-growing city. Key opportunities:
- **Rapid Development:** New neighborhoods require complete signage systems
- **City Centre Redevelopment:** Major civic projects underway
- **SkyTrain Extension:** Transit-related signage opportunities
- **Parks Expansion:** New parks and trails in growing areas

### Competitive Landscape
- Growing market attracts many competitors
- City values capacity to handle large projects
- Experience with similar-scale projects important

### Opportunity Patterns
- Development-related signage follows construction cycles
- Park projects often in spring budget allocations
- Transit projects tied to SkyTrain expansion timeline

### Growth Indicators
- Population growing ~2-3% annually
- Multiple new community centers planned
- Significant infrastructure investment ongoing

---

*Profile Version: 1.0*  
*Last Updated: December 2025*  
*Next Review: January 2025*
