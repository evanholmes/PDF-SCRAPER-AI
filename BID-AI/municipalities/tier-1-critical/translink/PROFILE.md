# TransLink - Regional Transit Authority Profile

## 🏛️ Basic Information

| Field | Value |
|-------|-------|
| **Official Name** | South Coast British Columbia Transportation Authority (TransLink) |
| **Type** | Regional Transit Authority |
| **Service Area** | Metro Vancouver (1,800 km²) |
| **Team ID** | TEAM-TL |
| **Tier** | 1 - Critical |
| **Calendar Color** | #C62828 (Deep Red) |
| **Status** | Priority |

---

## 🌐 Bid Portal Information

### Primary Portal: TransLink Procurement

| Field | Value |
|-------|-------|
| **Portal Name** | TransLink Procurement |
| **Portal URL** | https://www.translink.ca/about-us/doing-business-with-translink/procurement |
| **Portal Type** | Custom Portal / MERX |
| **Account Required** | Yes (MERX registration) |
| **Username** | [TO BE CONFIGURED] |
| **Password** | [SECURE STORAGE] |
| **MERX URL** | https://www.merx.com/ |

### Portal Features
- MERX integration for major procurements
- Direct postings on TransLink website
- Vendor pre-qualification programs
- Category-specific notifications

### Relevant Categories to Monitor
- Signage & Wayfinding
- Printing Services
- Passenger Information Displays
- Station Amenities
- Bus Shelter Equipment
- Marketing Materials

---

## 📋 Procurement Process

### Bid Types Used
- **RFP** (Request for Proposal) - Complex services
- **RFQ** (Request for Quotation) - Goods and simpler services
- **ITT** (Invitation to Tender) - Construction/installation
- **RFPQ** (Request for Pre-Qualification)
- **Standing Offers** - Ongoing supply agreements

### Typical Evaluation Criteria

| Criteria | Typical Weight |
|----------|----------------|
| Technical Approach | 35-45% |
| Experience & References | 20-30% |
| Price | 25-35% |
| Delivery/Schedule | 5-10% |
| Sustainability | 5-10% |

### Standard Requirements
- Valid Business License
- WorkSafeBC Registration
- Commercial General Liability ($5M minimum typical)
- Product liability (for manufactured goods)
- Performance bonds (larger contracts)
- Security clearance (for certain facilities)

---

## 🚌 Transit System Overview

### Infrastructure Requiring Signage

| Asset Type | Quantity | Signage Needs |
|------------|----------|---------------|
| SkyTrain Stations | 53+ | Wayfinding, passenger info, regulatory |
| Bus Exchanges | 20+ | Wayfinding, schedules, shelter signs |
| SeaBus Terminals | 2 | Wayfinding, marine regulatory |
| West Coast Express Stations | 8 | Commuter rail signage |
| Park & Rides | 25+ | Directional, regulatory |
| Bus Shelters | 6,000+ | Route info, advertising frames |
| Buses | 1,800+ | Interior/exterior signage |
| SkyTrain Cars | 400+ | Interior passenger information |

---

## 📅 Calendar Configuration

### Google Calendar Details
| Field | Value |
|-------|-------|
| Calendar Name | BID-AI: TransLink |
| Calendar ID | [TO BE CREATED] |
| Color | #C62828 (Deep Red) |
| Time Zone | America/Vancouver |

### Event Prefix
All events use prefix: `TL-[YEAR]-[NUMBER]`  
Example: `TL-2025-078`

---

## 🤖 Agent Team Configuration

### Team: TEAM-TL

```yaml
team_id: TEAM-TL
municipality: TransLink
tier: 1
priority: critical
type: transit_authority

scout_agent:
  scan_interval: 15  # minutes
  portal_urls:
    - https://www.translink.ca/about-us/doing-business-with-translink/procurement
    - https://www.merx.com/  # Secondary source
  keywords_profile: transit-extended
  alert_threshold: 30  # Lower threshold - high value opportunities
  scraper_type: custom

analyst_agent:
  priority_processing: true
  deep_analysis: true
  capability_threshold: 0.60
  transit_specialty: true
  large_volume_flag: true

writer_agent:
  template_set: translink-custom
  tone: professional-transit
  accessibility_focus: true
  safety_emphasis: true

compliance_agent:
  checklist: translink-standard
  multi_reviewer: true
  insurance_minimum: 5000000
  security_clearance: may_be_required
  bonding: likely_required
```

---

## 🏢 Key Departments & Contacts

### Procurement Services
- **Department:** Supply Chain Management
- **Website:** https://www.translink.ca/about-us/doing-business-with-translink
- **Vendor Inquiries:** vendorinquiry@translink.ca

### Relevant Divisions for Signage
- **Customer Communications** - Passenger information signage
- **Engineering** - Infrastructure signage
- **Real Estate & Development** - Station development signage
- **Bus Operations** - Bus shelter signage
- **Rail Operations** - SkyTrain station signage
- **Marketing** - Branded materials and signage

---

## 🚇 Major Expansion Projects

### Broadway Subway Project
- 6 new stations under construction
- Major signage contract opportunities
- Estimated completion: 2026
- Wayfinding, passenger info, regulatory signage needed

### Surrey-Langley SkyTrain
- 8 new stations planned
- Future major signage opportunity
- Estimated completion: 2028

### Bus Rapid Transit
- Various BRT corridors planned
- Station signage opportunities
- Ongoing program

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
translink/
├── PROFILE.md (this file)
├── portal-docs/
│   ├── procurement-policy.pdf
│   ├── vendor-registration-guide.pdf
│   ├── signage-standards.pdf
│   ├── accessibility-requirements.pdf
│   └── security-requirements.pdf
├── bids-active/
│   └── [active bid folders]
├── bids-archive/
│   └── [completed/passed bid folders]
├── proposals/
│   └── [submitted proposals]
├── templates/
│   └── translink-proposal-template.md
└── research/
    ├── expansion-projects.md
    ├── signage-specifications.md
    ├── station-inventory.md
    └── competitor-analysis.md
```

---

## 🔗 Important Links

- **Procurement Portal:** https://www.translink.ca/about-us/doing-business-with-translink/procurement
- **Doing Business Overview:** https://www.translink.ca/about-us/doing-business-with-translink
- **MERX Portal:** https://www.merx.com/
- **TransLink Projects:** https://www.translink.ca/plans-and-projects
- **Broadway Subway:** https://www.broadwaysubway.ca/
- **Accessibility:** https://www.translink.ca/rider-guide/accessible-transit

---

## 📝 Notes & Intelligence

### Strategic Importance
TransLink is a HIGH PRIORITY target due to:
- **Volume:** Extensive transit network requiring ongoing signage
- **Value:** Large contracts, often multi-year
- **Expansion:** Major projects (Broadway Subway, Surrey-Langley) represent significant opportunities
- **Recurring:** Bus shelter signage, station maintenance are ongoing needs

### Competitive Landscape
- Established transit signage vendors have incumbent advantage
- Pre-qualification often required
- Safety and accessibility compliance critical
- Union considerations for installation work

### Opportunity Patterns
- Major projects tied to expansion timelines
- Shelter signage contracts renewed periodically
- Station refresh projects ongoing
- Emergency/replacement signage year-round

### Key Considerations
- **Accessibility:** All signage must meet accessibility standards
- **Durability:** Transit environment requires robust materials
- **Safety:** Compliance with transit safety regulations
- **Branding:** Strict adherence to TransLink brand guidelines
- **Volume:** Capacity to produce large quantities on schedule

---

*Profile Version: 1.0*  
*Last Updated: December 2025*  
*Next Review: January 2025*
