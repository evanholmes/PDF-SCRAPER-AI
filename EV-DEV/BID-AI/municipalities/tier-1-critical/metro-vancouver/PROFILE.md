# Metro Vancouver - Regional District Profile

## 🏛️ Basic Information

| Field | Value |
|-------|-------|
| **Official Name** | Metro Vancouver Regional District |
| **Type** | Regional District (Federation of 21 municipalities) |
| **Population** | ~2.6 million (regional) |
| **Team ID** | TEAM-MV |
| **Tier** | 1 - Critical |
| **Calendar Color** | #4285F4 (Blue) |
| **Status** | Active |

---

## 🌐 Bid Portal Information

### Primary Portal: BidsAndTenders

| Field | Value |
|-------|-------|
| **Portal Name** | Metro Vancouver Bids and Tenders |
| **Portal URL** | https://metrovancouver.bidsandtenders.ca/Module/Tenders |
| **Portal Type** | BidsAndTenders Platform |
| **Account Required** | Yes |
| **Username** | [TO BE CONFIGURED] |
| **Password** | [SECURE STORAGE] |
| **Registration URL** | https://metrovancouver.bidsandtenders.ca/Registration |

### Portal Features
- Automated email notifications
- Saved searches by category
- Addenda notifications
- Online Q&A submission
- Document management
- Bid submission tracking

### Relevant Categories to Monitor
- Signs & Sign Making Equipment
- Printing & Publishing
- Construction Services
- Parks & Recreation
- Utilities
- Environmental Services

---

## 📋 Procurement Process

### Bid Types Used
- **RFP** (Request for Proposal)
- **RFQ** (Request for Quotation)
- **ITT** (Invitation to Tender)
- **RFEI** (Request for Expressions of Interest)
- **Standing Offers** (Pre-qualified vendor lists)

### Typical Evaluation Criteria

| Criteria | Typical Weight |
|----------|----------------|
| Technical Approach | 30-40% |
| Qualifications & Experience | 25-30% |
| Price | 25-35% |
| Sustainability | 5-10% |

### Standard Requirements
- Valid Business License
- WorkSafeBC Registration
- Commercial General Liability ($5M typical for regional projects)
- Environmental compliance
- References (minimum 3)

---

## 📅 Calendar Configuration

### Google Calendar Details
| Field | Value |
|-------|-------|
| Calendar Name | BID-AI: Metro Vancouver |
| Calendar ID | [TO BE CREATED] |
| Color | #4285F4 (Blue) |
| Time Zone | America/Vancouver |

### Event Prefix
All events use prefix: `MV-[YEAR]-[NUMBER]`  
Example: `MV-2025-045`

---

## 🤖 Agent Team Configuration

### Team: TEAM-MV

```yaml
team_id: TEAM-MV
municipality: Metro Vancouver Regional District
tier: 1
priority: critical
type: regional_district

scout_agent:
  scan_interval: 15  # minutes
  portal_url: https://metrovancouver.bidsandtenders.ca/Module/Tenders
  keywords_profile: extended
  alert_threshold: 35
  scraper_type: bidsandtenders
  multi_category: true

analyst_agent:
  priority_processing: true
  deep_analysis: true
  capability_threshold: 0.65
  regional_scope: true  # Affects multiple municipalities

writer_agent:
  template_set: metro-vancouver-custom
  tone: professional-regional
  sustainability_focus: true

compliance_agent:
  checklist: metro-vancouver-standard
  multi_reviewer: true
  insurance_minimum: 5000000
  environmental_compliance: required
```

---

## 🏢 Key Departments & Contacts

### Procurement Services
- **Department:** Financial Services - Procurement
- **Website:** https://metrovancouver.org/about-us/careers-business-opportunities
- **Email:** Via tender documents

### Relevant Service Areas for Signage
- **Regional Parks** - Park wayfinding, trail signage (extensive system)
- **Liquid Waste Services** - Facility signage
- **Solid Waste Services** - Transfer station signage
- **Water Services** - Utility and facility signage
- **Housing** - Metro Vancouver Housing signage

---

## �� Regional Parks System

Metro Vancouver manages 23 regional parks - major signage opportunity:

| Park | Size | Signage Potential |
|------|------|-------------------|
| Pacific Spirit | 763 ha | High - Trail wayfinding |
| Burnaby Lake | 311 ha | High - Multi-use trails |
| Colony Farm | 260 ha | Medium - Nature interpretation |
| Belcarra | 1,115 ha | High - Wilderness wayfinding |
| Minnekhada | 204 ha | Medium - Heritage interpretation |
| Campbell Valley | 535 ha | High - Equestrian & trail |
| Boundary Bay | 126 ha | Medium - Wildlife interpretation |
| And 16 more... | Various | Various |

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
metro-vancouver/
├── PROFILE.md (this file)
├── portal-docs/
│   ├── procurement-policy.pdf
│   ├── vendor-registration-guide.pdf
│   ├── sustainability-requirements.pdf
│   └── insurance-requirements.pdf
├── bids-active/
│   └── [active bid folders]
├── bids-archive/
│   └── [completed/passed bid folders]
├── proposals/
│   └── [submitted proposals]
├── templates/
│   └── metro-vancouver-proposal-template.md
└── research/
    ├── regional-parks-inventory.md
    ├── service-areas-overview.md
    └── sustainability-standards.md
```

---

## 🔗 Important Links

- **Main Procurement Portal:** https://metrovancouver.bidsandtenders.ca/Module/Tenders
- **Business Opportunities:** https://metrovancouver.org/about-us/careers-business-opportunities
- **Regional Parks:** https://metrovancouver.org/parks
- **About Metro Vancouver:** https://metrovancouver.org/about-us

---

## 📝 Notes & Intelligence

### Strategic Importance
Metro Vancouver is a regional district governing 21 municipalities. Key opportunities:
- **Regional Parks System:** 23 parks with extensive trail networks needing wayfinding
- **Utility Facilities:** Water, waste, and housing facilities require signage
- **Regional Consistency:** Projects often require consistent signage across multiple sites
- **Large Contract Values:** Regional scope means larger project values

### Competitive Landscape
- Larger contracts attract major competitors
- Regional scope requires demonstrated capacity
- Sustainability credentials increasingly important
- Experience with multi-site projects valued

### Opportunity Patterns
- Regional parks signage often in capital budget cycles
- Facility signage tied to construction/renovation projects
- Standing offers for ongoing maintenance work

### Member Municipalities
Metro Vancouver includes: Vancouver, Surrey, Burnaby, Richmond, Coquitlam, Delta, North Vancouver (City & District), West Vancouver, New Westminster, Port Coquitlam, Port Moody, Maple Ridge, Pitt Meadows, Langley (City & Township), White Rock, Bowen Island, Anmore, Belcarra, Lions Bay, Electoral Area A

---

*Profile Version: 1.0*  
*Last Updated: December 2025*  
*Next Review: January 2025*
